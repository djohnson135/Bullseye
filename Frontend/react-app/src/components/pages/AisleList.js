import React, { useState, useContext, useEffect } from "react";
import NavigationBar from "../NavigationBar";
import Footer from "../Footer";
import CheckboxTree from "react-checkbox-tree";
import "react-checkbox-tree/lib/react-checkbox-tree.css";
import GlobalContext from "../../context/GlobalContext";
import AisleListSection from "../AisleListSection";

export default function AisleList() {
  return (
    <div>
      <NavigationBar />
      <AisleListSection />
      <Footer />
    </div>
  );
}
