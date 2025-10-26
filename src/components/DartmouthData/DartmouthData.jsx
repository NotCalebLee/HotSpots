import React from "react";
import "./DartmouthData.css";

const DartmouthData = () => {
  return (
    <div id="dartmouth" className="dartmouth-section">
      <div className="dartmouth-title">
        <h1>Dartmouth Data</h1>
        <p className="dartmouth-subtitle">
          Interactive campus-wide Wi-Fi heatmap showing access point distribution across Dartmouth College
        </p>
      </div>
      
      <div className="dartmouth-visualization">
        <iframe
          src="/interactive_campus_heatmap.html"
          title="Dartmouth Campus Interactive Heatmap Visualization"
          className="dartmouth-iframe"
          loading="lazy"
        />
      </div>
    </div>
  );
};

export default DartmouthData;

