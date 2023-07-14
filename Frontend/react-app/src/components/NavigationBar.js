import React, { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { Link } from "react-router-dom";
import Dropdown from "react-bootstrap/Dropdown";
import "./NavigationBar.css";
import GoogleOuath from "./GoogleOuath";
import { authorize, backend_url } from "./Global";

function Navbar(props) {
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

  const [user, setUser] = useState(null);
  let authorizeHeader = "Bearer " + authorize.access_token;

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
  return (
    <>
      <nav className="navbar">
        <div className="navbar-container">
          <Link
            to="/Home"
            style={{ textDecoration: "none" }}
            className="navbar-logo"
          >
            <img src="/img/Bullseye-removebg.png" alt="Bullseye Logo" />
            &nbsp;Bullseye
          </Link>

          <ul className="nav-menu">
            <li className="nav-item">
              <Link
                to="/Home"
                style={{ textDecoration: "none" }}
                className="nav-links"
              >
                <div className="navFont">Home</div>
              </Link>
            </li>

            <li className="nav-item">
              <Link
                to="/List"
                style={{ textDecoration: "none" }}
                className="nav-links"
              >
                <div className="navFont">List</div>
              </Link>
            </li>

            <li className="nav-item">
              <Link
                to="/Path"
                style={{ textDecoration: "none" }}
                className="nav-links"
              >
                <div className="navFont">Path</div>
              </Link>
            </li>

            <li className="nav-item">
              <Link
                to="/AisleList"
                style={{ textDecoration: "none" }}
                className="nav-links"
              >
                <div className="navFont">Sequence</div>
              </Link>
            </li>

            <li className="nav-item">
              <div className="nav-item-signIn-name">
                <div>
                  {user?.fname} {user?.lname}
                </div>
              </div>
            </li>

            <li className="nav-item">
              <div className="nav-item-signIn">
                <GoogleOuath />
              </div>
            </li>
          </ul>
        </div>
      </nav>
    </>
  );
}

export default Navbar;
