import React from "react";
import { Route, Routes, BrowserRouter as Router } from "react-router-dom";
import classes from "./App.module.css";
import MainSection from "./components/MainSection";
import Banner from "./components/Banner";
import About from "./components/About";

function App() {
  return (
    <div id="home" className={classes.App}>
      <Router>
        <div className={classes.banner}>
          <Banner />
        </div>
        <div className={classes.backgroundimage}>
          <Routes>
            <Route
              path="/"
              element={
                <div className={classes.content}>
                  <MainSection />
                </div>
              }
            />
            <Route
              path="/about"
              element={
                <div className={classes.content}>
                  <About />
                </div>
              }
            />
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;