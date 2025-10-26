import React from "react";
import "./About.css";

const About = () => {
  // Use dynamic imports with fallback for static images
  const dartHeatmap = new URL("../../assets/dart_heatmap.png", import.meta.url)
    .href;
  const hkHeatmap = new URL("../../assets/Heat-Map2.jpg", import.meta.url).href;
  // Note: Replace Heat-Map2.jpg with hk_heatmap.png once generated

  return (
    <div id="about" className="about">
      <div className="about-title">
        <h1>Sample Data</h1>
      </div>
      <div className="about-sections">
        <div className="about-left">
          <p>Dartmouth Wi-Fi Heat Map</p>
          <img
            src={dartHeatmap}
            alt="Dartmouth campus Wi-Fi heatmap showing network usage patterns"
          />
        </div>
        <div className="about-right">
          <div className="about-para">
            <p>Hong Kong Wi-Fi Heat Map</p>
            <img
              src={hkHeatmap}
              alt="Hong Kong campus Wi-Fi heatmap showing network usage patterns"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
