import os
import cv2
import numpy as np
import seaborn as sns
from .map_scrape import scrape_map
from matplotlib import pyplot as plt
from svgpathtools import svg2paths


# gets rid of problematic 'blobs' associated with bounding boxes
def remove_blobs(map_data, aisle_locs):
    for aisle in aisle_locs:
        x, y = aisle[0], aisle[1]
        dx, dy, accessible, visited = 1, 1, False, set()
        while not accessible:
            blob_data = []
            for i in range(x - dx, x + dx + 1):
                for j in range(y - dy, y + dy + 1):
                    if i == j == 0:
                        continue
                    else:
                        try:
                            if map_data[j][i] == "#":
                                blob_data.append((j, i))
                                visited.add((j, i))
                            elif map_data[j][i] != ".":
                                continue
                            elif (j, i) not in visited:
                                accessible = True

                        except Exception as e:
                            continue

                if accessible:
                    break

            if not accessible:
                for loc in blob_data:
                    map_data[loc[0]][loc[1]] = "."

                dx, dy = dx + 1, dy + 1

    return map_data


# given the url for a store map, this method generates a matrix representation of the map
# note - this method returns two items: (i) a dictionary containing all aisle labels (along with the entrance 'E') and their (x, y) coordinates on the map;
# (ii) a numpy matrix representing the store map (e.g., aisle locations, the entrance location, and traversable/untraversable areas of the store)
# note: '.' denotes that an area is traversable; '#' denotes that an area is not traversable; 'E' denotes the entrance; everything else represents an aisle label


def create_map(url):
    # note: mapping for aisle data is of the form - A1: 101.0, A2: 102.0, ...
    # aisle_locs has keys that are the float representation of aisles and values of the form [aisle label, (x, y) coordinate]
    # entrance_loc is represented by the float 100.0 in the matrix
    map_file = scrape_map(url)
    entrance_loc, aisle_locs, aisle_cnt = (0, 0), {}, 101.0

    # parse contents found inside '<g id="content">' to extract useful data from online store map
    wall_shapes, reg_shapes, aisle_shapes, aisle_names = False, False, False, False
    for line in map_file.splitlines():
        if "Wall-Shapes" in line:
            wall_shapes, reg_shapes, aisle_shapes, aisle_names = (
                True,
                False,
                False,
                False,
            )

            wall_shapes_file = open("wall_shapes.txt", "a")
            wall_shapes_file.write("<g>\n")
            wall_shapes_file.close()
        elif "Register-Shapes" in line:
            wall_shapes, reg_shapes, aisle_shapes, aisle_names = (
                False,
                True,
                False,
                False,
            )

            reg_shapes_file = open("reg_shapes.txt", "a")
            reg_shapes_file.write("<g>\n")
            reg_shapes_file.close()
        elif "Aisle-Shapes" in line:
            wall_shapes, reg_shapes, aisle_shapes, aisle_names = (
                False,
                False,
                True,
                False,
            )

            aisle_shapes_file = open("aisle_shapes.txt", "a")
            aisle_shapes_file.write("<g>\n")
            aisle_shapes_file.close()
        elif "Aisle-Names" in line:
            wall_shapes, reg_shapes, aisle_shapes, aisle_names = (
                False,
                False,
                False,
                True,
            )
        elif "</g>" in line:
            if wall_shapes:
                wall_shapes_file = open("wall_shapes.txt", "a")
                wall_shapes_file.write("</g>\n")
                wall_shapes_file.close()
            elif reg_shapes:
                reg_shapes_file = open("reg_shapes.txt", "a")
                reg_shapes_file.write("</g>\n")
                reg_shapes_file.close()
            elif aisle_shapes:
                aisle_shapes_file = open("aisle_shapes.txt", "a")
                aisle_shapes_file.write("</g>\n")
                aisle_shapes_file.close()

            wall_shapes, reg_shapes, aisle_shapes, aisle_names = (
                False,
                False,
                False,
                False,
            )
        else:
            # process data here
            # create files for paths of wall_shapes, reg_shapes, and aisle_shapes
            # don't forget to log entrance loc (and maybe restrooms, guest services, Starbucks, pharmacy, etc. in the future)
            if wall_shapes:
                # data stored in separate file for 'svg2paths'
                wall_shapes_file = open("wall_shapes.txt", "a")
                wall_shapes_file.write(line)
                wall_shapes_file.close()
            elif reg_shapes:
                # data stored in separate file for 'svg2paths'
                reg_shapes_file = open("reg_shapes.txt", "a")
                reg_shapes_file.write(line)
                reg_shapes_file.close()
            elif aisle_shapes:
                # data stored in separate file for 'svg2paths'
                aisle_shapes_file = open("aisle_shapes.txt", "a")
                aisle_shapes_file.write(line)
                aisle_shapes_file.close()
            elif aisle_names:
                # get (x, y) locs of aisle names
                info = line.split(" ")[7:9]
                x = int(float(info[0][3:-1]) * 100)
                y = int(float(info[1][3:-1]) * 100)

                # get label associated with aisles
                label, idx = "", 0
                while line.split(" ")[-1][idx] != ">":
                    idx += 1
                label = line.split(" ")[-1][idx + 1 :]
                idx2 = label.find("<")
                label = label[:idx2]

                aisle_locs[aisle_cnt] = [label, (x, y)]
                aisle_cnt += 1
            elif "entrance" in line:
                # get (x, y) loc of entrance text
                info = line.split(" ")[-3:-1]
                x = int(float(info[0][3:-1]) * 100)
                y = int(float(info[1][3:-1]) * 100)
                entrance_loc = (x, y)

    # get path data associated with all relevant store aspects
    wall_paths, wall_attributes = svg2paths("wall_shapes.txt")
    reg_paths, reg_attributes = svg2paths("reg_shapes.txt")
    aisle_paths, aisle_attributes = svg2paths("aisle_shapes.txt")

    # get bounds of all relevant paths
    wall_bounds_init, reg_bounds_init, aisle_bounds_init = (
        [path.bbox() for path in wall_paths],
        [path.bbox() for path in reg_paths],
        [path.bbox() for path in aisle_paths],
    )
    wall_bounds, reg_bounds, aisle_bounds = [], [], []

    # scale up the data so it can be represented in our matrix
    for bound in wall_bounds_init:
        wall_bounds.append(
            (
                int(bound[0] * 100),
                int(bound[1] * 100),
                int(bound[2] * 100),
                int(bound[3] * 100),
            )
        )

    # store upper/lower/left/right bounds of map so we can use these as offsets in our matrix representation
    map_xmin, map_xmax, map_ymin, map_ymax = wall_bounds[0]
    map_data = np.full((map_ymax - map_ymin, map_xmax - map_xmin), 0, dtype=float)

    # finish scaling up the data so it can be represented in our matrix
    for bound in reg_bounds_init:
        reg_bounds.append(
            (
                int(bound[0] * 100) - map_xmin,
                int(bound[1] * 100) - map_xmin,
                int(bound[2] * 100) - map_ymin,
                int(bound[3] * 100) - map_ymin,
            )
        )

    for bound in aisle_bounds_init:
        aisle_bounds.append(
            (
                int(bound[0] * 100) - map_xmin,
                int(bound[1] * 100) - map_xmin,
                int(bound[2] * 100) - map_ymin,
                int(bound[3] * 100) - map_ymin,
            )
        )

    # create blocks/boundaries that represent areas that aren't traversable
    all_bounds, boundaries = reg_bounds + aisle_bounds, []
    for bound in all_bounds:
        xmin, xmax, ymin, ymax = bound[0], bound[1], bound[2], bound[3]
        boundaries.append(np.full((ymax - ymin, xmax - xmin), 1, dtype=float))

    # add blocks/boundaries to matrix representation of map
    for i in range(len(boundaries)):
        bound, boundary = all_bounds[i], boundaries[i]
        xmin, xmax, ymin, ymax = bound[0], bound[1], bound[2], bound[3]
        map_data[ymin:ymax, xmin:xmax] = boundary

    # condense matrix representation of map
    scale, (y, x) = 40, map_data.shape
    map_data = cv2.resize(
        map_data, dsize=(x // scale, y // scale), interpolation=cv2.INTER_CUBIC
    )

    # allows us to visualize matrix representation of map (matrix data must be float) [TODO: uncomment below to see]
    # # add aisle and entrance data to map (this is described at the top of this file)
    # map_data[
    #     (entrance_loc[1] - map_ymin) // scale, (entrance_loc[0] - map_xmin) // scale
    # ] = 100.0
    # for aisle in aisle_locs:
    #     col, row = (aisle_locs[aisle][1][0] - map_xmin) // scale, (
    #         aisle_locs[aisle][1][1] - map_ymin
    #     ) // scale
    #     map_data[row, col] = aisle / 1000  # '/ 1000 was added'

    # plt.imshow(map_data, interpolation="nearest", vmin=0, vmax=1)
    # plt.show()

    # translate float data in matrix representation of map to more understandable string data
    # note: '.' denotes that an area is traversable; '#' denotes that an area is not traversable; 'E' denotes the entrance; everything else represents an aisle label
    map_data = np.array(np.absolute(np.round(map_data)) * 1.0).astype(str)
    map_data[map_data == "0.0"] = "."
    map_data[map_data == "1.0"] = "#"
    map_data[
        (entrance_loc[1] - map_ymin) // scale, (entrance_loc[0] - map_xmin) // scale
    ] = "E"

    for aisle in aisle_locs:
        col, row = (aisle_locs[aisle][1][0] - map_xmin) // scale, (
            aisle_locs[aisle][1][1] - map_ymin
        ) // scale
        map_data[row, col] = aisle_locs[aisle][0]

    # store label locations for search algorithm's use
    label_locs = {
        "E": (
            (entrance_loc[0] - map_xmin) // scale,
            (entrance_loc[1] - map_ymin) // scale,
        )
    }

    for aisle in aisle_locs:
        col, row = (aisle_locs[aisle][1][0] - map_xmin) // scale, (
            aisle_locs[aisle][1][1] - map_ymin
        ) // scale

        label_locs[aisle_locs[aisle][0]] = (col, row)

    # resolve potential 'blob' issues in matrix representation of map
    map_data = remove_blobs(map_data, label_locs.values())

    # clean up intermediate files
    os.remove("wall_shapes.txt")
    os.remove("reg_shapes.txt")
    os.remove("aisle_shapes.txt")

    return (label_locs, map_data)


# testing below [TODO: uncomment below to test]
# label_locs, map_data = create_map("https://www.target.com/sl/college-station/800")

# # output matrix representation of map to 'res_matrix.txt' [TODO: delete this file after viewing/confirming results]; display label location data
# np.savetxt("res_matrix.txt", map_data, fmt="%3s")
# print(label_locs)
