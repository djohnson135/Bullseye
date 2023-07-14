import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Path from "./components/pages/Path";
import Home from "./components/pages/Home";
import Landing from "./components/pages/Landing";
import List from "./components/pages/List";
import AisleList from "./components/pages/AisleList";
import ScrollToTop from "./components//ScrollToTop";
import React from "react";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <ScrollToTop />
        <Routes>
          <Route path="/" exact element={<Landing />} />
          <Route path="/Home" element={<Home />} />
          <Route path="/Path" element={<Path />} />
          <Route path="/List" element={<List />} />
          <Route path="/AisleList" element={<AisleList />} />
          <Route
            exact
            path="docs.html"
            render={() => {
              window.location.href = "docs.html";
            }}
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
