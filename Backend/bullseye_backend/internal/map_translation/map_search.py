import numpy as np
import heapq
import re
import time
from PIL import Image, ImageDraw
import boto3
import io

S3_CLIENT = boto3.client('s3')

def douglas_peucker(points, tolerance):
    # Find the point farthest from the line segment between the start and end points
    dmax = 0
    index = 0
    for i in range(1, len(points) - 1):
        d = perpendicular_distance(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d

    # If the farthest point is within the tolerance, return the start and end points
    if dmax <= tolerance:
        return [points[0], points[-1]]

    # Otherwise, recursively simplify the two parts of the path
    left = douglas_peucker(points[: index + 1], tolerance)
    right = douglas_peucker(points[index:], tolerance)

    # Combine the two simplified paths into a single path
    return left[:-1] + right


def perpendicular_distance(point, start, end):
    # Calculate the perpendicular distance of a point from the line segment between start and end
    x0, y0 = point
    x1, y1 = start
    x2, y2 = end
    numer = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denom = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return numer / denom


class Node:
    def __init__(self, matrix, x, y, g, h, aisles=None, parent=None):
        self.matrix = matrix
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = g + h
        self.aisles = aisles
        self.parent = parent

    def __lt__(self, other):
        return self.f <= other.f


# Heuristic for getting to aisles
def heuristic(x, y, aisles,shape,checkouts, dx, dy):
    h=[]
    # Use manhattan distance to find best path to closest aisle
    for a in aisles:
        h.append(1.01*abs(x - aisles[a][0])//1 + abs(y - aisles[a][1]))
    h = shape[0]*min(h)
    # biases heuristic towards diagonal movement
    # This allows for figure-8 type paths while preventing loops
    if abs(x-dx) + abs(y-dy) == 1:
        h+=2
    # Biases heuristic towards keeping visited aisles in path
    # Because we want to find a path through all possible aisles
    h += shape[0]**2*shape[1]**2*len(aisles)
    return h


# Heuristic for getting to checkout
def heuristic_2(x, y, shape, checkouts):
    h = []
    # Use manhattan distance to find best path to closest checkout lane
    for c in checkouts:
        h.append(abs(x - checkouts[c][0]) + abs(y - checkouts[c][1]) // 2)
    h = (shape[0]) * min(h)
    return h


# Gets all possible child nodes from current position
def get_neighbors(matrix, node, aisles):
    neighbors = []
    rows, cols = (matrix).shape
    x, y = node.x, node.y
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if nx < 0 or ny < 0 or nx >= rows or ny >= cols:
            continue
        if matrix[nx, ny] == "#":
            continue
        neighbors.append(Node(matrix, nx, ny, node.g + 1, node.h, aisles))
    return neighbors


# A* Algorithm for going from last aisle to checkout
# "Goal node" would be getting to a "CL" from starting location
def A_star_2(matrix, start, checkouts, start_time):
    start_node = Node(matrix,start[0], start[1],0, 0)
    open_list = [start_node]
    final_coordinate = ()
    visited = {(start_node.x, start_node.y): 0}
    while open_list:
        # current_time = time.time()
        # if current_time-start_time > 12:
        #     print("Timeout.")
        #     exit()
        current_node = heapq.heappop(open_list)
        previous_value = current_node.matrix[current_node.x, current_node.y]
        current_node.matrix[current_node.x, current_node.y] = "*"

        if ("CL" in previous_value):
            goal_node = current_node
            final_coordinate = (current_node.x, current_node.y)
            break

        neighbors = get_neighbors(current_node.matrix, current_node,current_node.aisles)
        for neighbor in neighbors:
            neighbor.h = heuristic_2(neighbor.x, neighbor.y,matrix.shape,checkouts)
            if (neighbor.x, neighbor.y) not in visited or neighbor.h < visited[(neighbor.x, neighbor.y)]:
                # neighbor.h = heuristic_2(neighbor.x, neighbor.y,matrix.shape,checkouts)
                neighbor.parent = current_node
                heapq.heappush(open_list, neighbor)
                visited[(neighbor.x, neighbor.y)] = neighbor.h
        
    if goal_node is None:
        return None

    path = []
    while goal_node is not None:
        path.append((goal_node.x, goal_node.y))
        goal_node = goal_node.parent
    return path[::-1], final_coordinate

# A* Algorithm for going from enterance to each aisle
# "Goal node" would be getting all aisles covered
def A_star(matrix, aisles,enter_coords,checkouts,start_time):
    start_node = Node(matrix,enter_coords[0], enter_coords[1], 0, 0,aisles)
    found = []
    open_list = [start_node]
    final_coordinate = ()
    visited = {(start_node.x, start_node.y): 0}
    goal_node = None
    while open_list:
        # current_time = time.time()
        # if current_time-start_time > 240:
        #     print("Timeout.")
        #     exit()
        current_node = heapq.heappop(open_list)
        previous_value = current_node.matrix[current_node.x, current_node.y]
        current_node.matrix[current_node.x, current_node.y] = "*"

        if previous_value in (current_node.aisles).keys():
                current_node.aisles.pop(previous_value)
                found.append(previous_value)

        if len(current_node.aisles) == 0:
            goal_node = current_node
            final_coordinate = (current_node.x, current_node.y)
            break

        neighbors = get_neighbors(current_node.matrix, current_node,current_node.aisles)
        for neighbor in neighbors:
            neighbor.h = heuristic(neighbor.x, neighbor.y, neighbor.aisles,matrix.shape,checkouts, current_node.x, current_node.y)
            if (neighbor.x, neighbor.y) not in visited or neighbor.h < visited[(neighbor.x, neighbor.y)]:
                # neighbor.h = heuristic(neighbor.x, neighbor.y, neighbor.aisles,matrix.shape,checkouts, current_node.x, current_node.y)
                neighbor.parent = current_node
                heapq.heappush(open_list, neighbor)
                visited[(neighbor.x, neighbor.y)] = neighbor.h
    
    if goal_node is None:
        return None
    
    path = []
    while goal_node is not None:
        path.append((goal_node.x, goal_node.y))
        goal_node = goal_node.parent

    return path[::-1], final_coordinate, found


def generate_images(
    path_f3, aisles, lines, final_coordinate, matrix_x, current_travel, s, order_id, aisle_name
):
    i = 0
    results = []
    for line in lines:
        results.append([])
        results[i] = line
        results_clone = []
        for j in results[i]:
            if j == "#":
                j = (0.45, 0.45, 0.45)
            elif j == "." or j == "*":
                j = (0.95, 0.95, 0.95)
            else:
                j = (0.5, 0, 0)
            results_clone.append(j)
        results[i] = results_clone
        i += 1
    
    for a in aisles:
        results[aisles[a][0]][aisles[a][1]] = (1, 0.84, 0)
    results[final_coordinate[0]][final_coordinate[1]] = (0.50, 0.98, 0.71)
    
    results = np.array(results)
    
    img = Image.fromarray(np.uint8(results * 255), "RGB")

    img1 = ImageDraw.Draw(img)
    img1.line(path_f3, fill="red", width=2)
    directions = [
        (0, 0),
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (-1, -1),
        (1, -1),
        (-1, 1),
        (1, 1),
    ]
    
    for a in aisles:
        if ((aisles[a][1], aisles[a][0]) in path_f3) or (
            (aisles[a][1], aisles[a][0]) in current_travel
        ):
            
            for dx, dy in directions:
                nx, ny = aisles[a][1] + dx, aisles[a][0] + dy
                if (
                    nx < 0
                    or ny < 0
                    or nx >= matrix_x.shape[1]
                    or ny >= matrix_x.shape[0]
                ):
                    continue
                else:
                    img.putpixel((nx, ny), (255, 215, 0))
            current_travel.append((aisles[a][1], aisles[a][0]))
    if (final_coordinate[1], final_coordinate[0]) in path_f3:
        for dx, dy in directions:
            nx, ny = final_coordinate[1] + dx, final_coordinate[0] + dy
            if nx < 0 or ny < 0 or nx >= matrix_x.shape[1] or ny >= matrix_x.shape[0]:
                continue
            else:
                img.putpixel((nx, ny), (127, 239, 182))
    # img.show() used for debugging locally
    # img.show()
    # img.save("path_" + str(s) + ".png", quality=100)
    img = img.resize((img.size[0] * 10, img.size[1] * 10), resample=Image.BOX)
    mem_file = io.BytesIO()
    img.save(mem_file, format="PNG", quality=100)
    mem_file.seek(0)
    S3_CLIENT.put_object(
        Bucket="bullseye-path-images",
        Key=f"{order_id}/{aisle_name}.png",
        Body=mem_file,
        ContentType='image/png',
    )
    
    return current_travel


# Main function, use this for the main in the lambda function
def search(matrix, cart_aisles, order_id):
    matrix_x = np.array(matrix)

    def reverseTuple(lstOfTuple):
        return [tup[::-1] for tup in lstOfTuple]

    aisles = {}
    checkouts = {}
    enter_coords = {}
    # Replace with list of item aisles from Chrome Extension outputs
    options = cart_aisles
    for i in range(len(matrix_x)):
        for j in range(len(matrix_x[i])):
            x = matrix_x[i][j]
            for k in options:
                if (k == x):
                    aisles[x] = (i, j)
                if ("E" in x):
                    enter_coords = (i, j)
                if ("CL" in x):
                    checkouts[x] = (i, j)

    start_time = time.time()
    path1, part1_coordinate, found = A_star(
        matrix_x.copy(), aisles.copy(), enter_coords, checkouts, start_time
    )
    path2, final_coordinate = A_star_2(
        matrix_x.copy(), part1_coordinate, checkouts, start_time
    )
    path = path1 + path2
    end_time = time.time()
    if path is None:
        print("No path found.")
    else:
        print("Path found")
    subpaths = []
    sorted_aisles = []
    for i in range(len(found)):
        subpaths.append([])
        for p in path:
            subpaths[i].append(p)
            if aisles[found[i]] == p:
                sorted_aisles.append(found[i])
                subpaths[i].append(p)
                break
    subpaths.append(path)
    sorted_aisles.append("checkout")

    for p in path:
        matrix_x[p] = "*"

    elapsed_time = end_time - start_time
    current_travel = []

    for sp, s in zip(subpaths, range(len(subpaths))):
        path_f3 = reverseTuple(douglas_peucker(sp, 1.7))
        current_travel = generate_images(
            path_f3,
            aisles,
            list(matrix_x),
            final_coordinate,
            matrix_x,
            current_travel,
            s,
            order_id,
            sorted_aisles[s]
        )
        
    print("Elapsed time: ", elapsed_time)
    print(sorted_aisles)
    return sorted_aisles