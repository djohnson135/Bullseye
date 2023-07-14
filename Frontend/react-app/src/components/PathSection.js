import React from "react";
import "./PathSection.css";
import { useState, useEffect } from "react";
import { authorize, backend_url } from "./Global";

function PathSection() {
  const [order, setOrder] = useState(null);
  useEffect(() => {
    const request = {
      mode: "cors",
      method: "GET",
      headers: {
        Authorization: "Bearer " + authorize.access_token,
        "Access-Control-Allow-Origin": "*"
      },
      credentials: "include",
    };
    fetch(`${backend_url}/order/recent`, request)
      .then((response) => response.json())
      .then((data) => setOrder(data));
  }, []);
  let orderNum = null;
  if (order != null) {
    if (order.order_num != null) {
      orderNum = order?.order_num;
    }
    var aisleList = order.ailse_order?.map(function (aisle) {
      let s3url =
        "https://bullseye-path-images.s3.us-east-2.amazonaws.com/" +
        orderNum +
        "/" +
        aisle +
        ".png";
      let aisleTitle = `Aisle ${aisle}`;
      if (aisle === "checkout") {
        aisleTitle = "Checkout";
      }
      return (
        <div>
          <div className="font-semibold text-xl py-[1%]">
            {aisleTitle}
          </div>
          <img className="imgSize" src={s3url} />
        </div>
      );
    });
  }

  const [user, setUser] = useState(null);

  useEffect(() => {
    const request = {
      mode: "cors",
      method: "GET",
      headers: {
        Authorization: "Bearer " + authorize.access_token,
        "Access-Control-Allow-Origin": "*"
      },
      credentials: "include",
    };
    fetch(`${backend_url}/user/`, request)
      .then((response) => response.json())
      .then((data) => setUser(data));
  }, []);

  if (authorize.userLoggedIn === false) {
  return (
    <div>
      <div className="path-wrapper2">
        <center>
          <div className="path-header2">
            <p>
               Please Sign in first to see <span className="path-red">Bullseye's</span> optimal path!
            </p>
          </div>
          <div className="path-bg">
            {aisleList}
          </div>
        </center>
      </div>
    </div>
  );
  }
  else {
    return (
      <div>
        <div className="path-wrapper">
          <center>
            <div className="path-header">
              <p>
                <span className="path-red">Bullseye's</span> Optimal In-Store Path
              </p>
            </div>
            <div className="path-bg">
              {aisleList}
            </div>
          </center>
        </div>
      </div>
    );
  }
}

export default PathSection;
