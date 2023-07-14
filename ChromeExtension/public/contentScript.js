if (typeof init === "undefined") {
  /**
   * Content script initialization function that checks if the user is on the page https://www.target.com/cart. If so, it uses JavaScript's querySelectorAll to obtain the html tags containing the tcin data, zipcode, and 
   * store name of the user's products in their cart. Then sends this to background.js through chrome.extension's runtime.sendMessage function 
   * @returns {Array} info: List of the user's various product id's (TCIN's), followed by their store name, and finally their store zipcode
   */
  const init = function () {
    setTimeout(() => {
      console.log(document.URL);

      if (document.URL == "https://www.target.com/cart") {
        const x = document.querySelectorAll("[data-tcin]");
        const zip = document.querySelectorAll("#zip-code-id-btn");
        const store = document.querySelectorAll("#web-store-id-msg-btn");
        let info = [];

        for (const name of x) {
          info.push(name.getAttribute("data-tcin"));
        }
        info.push(zip[0].innerText);
        info.push(store[0].innerText);

        chrome.runtime.sendMessage({ greeting: info }, function (response) {
          console.log(response.farewell);
        });
      } else {
        const x = document.querySelectorAll("div > b");

        for (const name of x) {
          if (name.innerHTML == "TCIN") {
            var currentTCIN = name.nextSibling.nextSibling.textContent;
          }
        }

        const y = document.querySelectorAll("button");

        for (const name of y) {
          if (name.getAttribute("data-test") == "shippingButton") {
            var addButton = name;
          }
        }
        addButton.addEventListener("click", function () {
          alert("ADDED TO GENERATION");
          chrome.runtime.sendMessage(
            { greeting: currentTCIN },
            function (response) { }
          );
        });
      }
    }, 3000);
  };
  init();
}
