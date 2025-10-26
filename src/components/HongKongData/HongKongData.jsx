import React from "react";
import "./HongKongData.css";

const HongKongData = () => {
  return (
    <div id="hongkong" className="hongkong-section">
      <div className="hongkong-title">
        <h1>Hong Kong Data</h1>
        <p className="hongkong-subtitle">
          Interactive 3D visualization of HKU Library Wi-Fi traffic across multiple floors
        </p>
      </div>
      
      <div className="hongkong-visualization">
        <iframe
          src="/hku_library_3d_floors.html"
          title="HKU Library 3D Floors Interactive Visualization"
          className="hongkong-iframe"
          loading="lazy"
        />
      </div>
    </div>
  );
};

export default HongKongData;

