import React from "react";
import "./Desc.css";
import HeatMap from "../../assets/Heat-Map2.jpg";
import AnchorLink from "react-anchor-link-smooth-scroll";
const Hero = () => {
  return (
    <div id="home" className="hero">
      <img src={HeatMap} alt="" />
      <h1>
        <span>HotSpots</span> 
      </h1>
      <p>Interactive heatmap that visualizes network usage of a given area in real time</p>
      <div className="hero-action">
        <div className="hero-connect">
          <AnchorLink className="anchor-link" offset={50} href="#contact">
            Contact Us
          </AnchorLink>
        </div>
        <div className="hero-resume">
          <a
            href="/resume0225.pdf"
            target="_blank"
            rel="noopener noreferrer"
            className="anchor-link"
          >
            About us
          </a>
        </div>
      </div>
    </div>
  );
};

export default Hero;
