import React from "react";
import "./Desc.css";
import Logo from "../../assets/Resized_20251026_004217-removebg-preview.png";

const Hero = () => {
  return (
    <div id="home" className="hero">
      <img src={Logo} alt="HotSpots Logo" className="hero-logo" />
      <p>An interactive heatmap that visualizes network usage of a given area in real time</p>
    </div>
  );
};

export default Hero;
