import Head from "../Head";
import GoogleOuath from "../GoogleOuath";
import React, { useState, useContext } from "react";
import NavigationBar from "../NavigationBar";
import InfoSection from "../InfoSection";
import HeroSection from "../HeroSection";
import Footer from "../Footer";

const Home = (props) => {
  return (
    <div>
      <NavigationBar />
      <HeroSection />
      <InfoSection />
      <Footer />
    </div>
  );
};

export default Home;
