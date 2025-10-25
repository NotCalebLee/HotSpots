import { processData } from "./utils/dataProcessor.js";
import { renderHeatmap } from "./components/map.js";

// Fetch the sample data
fetch("data.json")
  .then((res) => res.json())
  .then((data) => {
    console.log("Loaded test data:", data);

    // Process the data
    const processed = processData(data);

    // Render the heatmap
    renderHeatmap(processed);
  })
  .catch((err) => console.error("Error loading test data:", err));
