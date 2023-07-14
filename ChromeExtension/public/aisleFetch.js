const API_KEY = "57482C072B994B1F8C13F85D48203DB0"; // [TODO] update this once we get paid tier

const getProductData = async (itemIDs, zipcode) => {
  // [TODO] implement zip code swapping (if necessary) so orders associated with stores not in our list can be processed
  const results = await Promise.all(
    itemIDs.map(async (id) => {
      // set up the request parameters
      const params = {
        api_key: API_KEY,
        type: "product",
        tcin: String(id),
        customer_zipcode: String(zipcode),
      };

      // make the http GET request to RedCircle API
      const res = await fetch("https://api.redcircleapi.com/request", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(params),
      });

      return res.data;
    })
  ).catch((error) => {
    // catch and print the error
    console.log(error);
  });

  let aisles = new Set();
  let tcin_data = {};
  resData = JSON.parse(JSON.stringify(results, 0, 2));

  for (let x of resData) {
    aisles.add(x.product.aisle);
    tcin_data[x.product.tcin] = {
      name: x.product.title,
      image: x.product.main_image.link,
      aisle: x.product.aisle,
    };
  }

  let store_loc = resData[0].location_info;

  console.log(resData[0].request_info);
  return { aisles, tcin_data, store_loc };
};

// testing here
// inputs are a list of TCIN numbers and the relevant store zip code
getProductData(
  ["14774450", "51140573", "14921217", "13159011", "76624144", "13330996"],
  "77840"
).then((results) => {
  console.log(results);
});
