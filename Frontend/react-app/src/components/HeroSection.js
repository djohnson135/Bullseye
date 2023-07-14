import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Carousel from "react-bootstrap/Carousel";
import { authorize, backend_url } from "./Global";
import "./HeroSection.css";

function HeroSection() {
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
        <div className="bg">
          <Carousel controls={false} indicators={false} fade>
            <Carousel.Item interval={6000}>
              <div className="bgImg-hero"></div>
              <div className="text-hero">
                <p>For Your Improved Shopping Experience,</p>
                <Link to="/Path">
                  <button class="learnMoreButton-hero" color="black">
                    GET STARTED
                  </button>
                </Link>
              </div>
              <Carousel.Caption></Carousel.Caption>
            </Carousel.Item>
            <Carousel.Item interval={6000}>
              <div className="bgImg-hero2"></div>
              <div className="text-hero2">
                <p>Get Bullseye,</p>
                <p>Save your time</p>
                <Link to="/Path">
                  <button class="learnMoreButton-hero2" color="black">
                    GET STARTED
                  </button>
                </Link>
              </div>
              <Carousel.Caption></Carousel.Caption>
            </Carousel.Item>
          </Carousel>
        </div>
      </div>
    );
  } else {
    return (
      <div>
        <div className="bg">
          <div className="bgImg-hero">
            {/* <img src="img/cart3.png" width="100%">
                    </img> */}
          </div>

          <div className="text-hero">
            <p>
              {user?.fname} {user?.lname}
            </p>
            <div className="p2">Welcome to Bullseye!</div>
            {/* <p><span className='hero-red'>Bullseye</span></p> */}
            <Link to="/Path">
              <button class="learnMoreButton-hero" color="black">
                GET STARTED
              </button>
            </Link>
          </div>
        </div>
      </div>
    );
  }
}

export default HeroSection;
