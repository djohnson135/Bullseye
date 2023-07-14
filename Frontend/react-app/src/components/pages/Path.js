import Head from "../Head";
import GoogleOuath from "../GoogleOuath";
import NavigationBar from "../NavigationBar";
import PathSection from "../PathSection";
import Footer from "../Footer";
import React, { useContext, useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { authorize, backend_url } from "../Global";
import GlobalContext from "../../context/GlobalContext";

function htmlDecode(input) {
  const textArea = document.createElement("textarea");
  textArea.innerHTML = input;
  return textArea.value;
}

const Path = (props) => {
  const {
    aisleListData,
    setAisleListData,
    sequenceData,
    setSequenceData,
    expanded,
    setExpanded,
  } = useContext(GlobalContext);

  const [user, setUser] = useState(null);
  const [searchParams, setSearchParams] = useSearchParams();

  let access_token = searchParams.get("access_token");
  let email = searchParams.get("user_email");

  if (access_token != null) {
    authorize.access_token = access_token;
    authorize.userLoggedIn = true;
  }
  if (email != null) {
    authorize.email = email;
  }

  useEffect(() => {
    const request = {
      mode: "cors",
      method: "GET",
      headers: {
        Authorization: "Bearer " + authorize.access_token,
        "Access-Control-Allow-Origin": "*",
      },
      credentials: "include",
    };
    fetch(`${backend_url}/user/`, request)
      .then((response) => response.json())
      .then((data) => setUser(data));
  }, []);

  // fetches ordered aisle list and all item data, then configures it such that it can be represented in a usable manner
  if (authorize.userLoggedIn && sequenceData.length === 0) {
    const request = {
      mode: "cors",
      method: "GET",
      headers: {
        Authorization: "Bearer " + authorize.access_token,
        "Access-Control-Allow-Origin": "*",
      },
      credentials: "include",
    };
    fetch(`${backend_url}/order/recent`, request)
      .then((response) => response.json())
      .then((results) => {
        let aisle_order = results.ailse_order; // FIXME
        let items = results.items;
        let sequence_data = [];

        // order 'sequence_data' based on 'aisle_order' list
        for (let i of aisle_order) {
          let aisle = { label: "Aisle " + i, value: i, children: [] };
          expanded.push(aisle.value);
          for (let j of items) {
            let labelText = `${htmlDecode(j.name)} (${j.price})`;
            if (j.aisle === i) {
              aisle["children"].push({
                label: (
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "row",
                      alignItems: "center",
                    }}
                  >
                    <img
                      src={j.image}
                      width="60px"
                      alt={labelText}
                      style={{
                        maxHeight: "60px",
                        marginRight: "10px",
                        border: "2px solid black",
                      }}
                    />
                    <p>{labelText}</p>
                  </div>
                ),
                value: htmlDecode(j.name),
              });
            }
          }
          sequence_data.push(aisle);
        }

        setSequenceData(sequence_data);

        let aisle_list_data = [];
        // order 'aisle_list_data' based on 'aisle_order' list
        for (let i of aisle_order) {
          for (let j of items) {
            if (j.aisle === i) {
              aisle_list_data.push([htmlDecode(j.name), j.aisle, j.price]);
            }
          }
        }

        setAisleListData(aisle_list_data);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  return (
    <div>
      <NavigationBar />
      <PathSection />
      <Footer />
    </div>
  );
};

export default Path;
