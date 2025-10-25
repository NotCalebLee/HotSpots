import React, { useState } from "react";
import { processData } from "./utils/dataProcessor.jsx";
import Heatmap from "./components/Heatmap";
import "../styles/style.css";

export default function App() {
  const [dataset, setDataset] = useState([]);
  const [processedData, setProcessedData] = useState([]);

  const handleUpload = async (event) => {
    const file = event.target.files?.[0];
    if (file) {
      const text = await file.text();
      const data = JSON.parse(text);
      setDataset(data);
    }
  };

  const handleUpdate = () => {
    if (dataset.length === 0) {
      alert("Please upload a dataset first!");
      return;
    }
    const processed = processData(dataset);
    setProcessedData(processed);
  };

  return (
    <div className="app-container">
      <header>
        <h1>Network Weather Map</h1>
        <p>Visualize Wi-Fi usage across your region</p>
      </header>

      <main>
        <section id="map-container">
          <Heatmap data={processedData} />
        </section>

        <section id="controls">
          <input
            type="file"
            accept=".json,.csv"
            onChange={handleUpload}
          />
          <button onClick={handleUpdate}>Update Map</button>
        </section>
      </main>

      <footer>
        <p>© 2025 Network Weather Map Project</p>
      </footer>
    </div>
  );
}
