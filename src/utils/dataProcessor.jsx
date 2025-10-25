export function processData(data) {
  // Example: convert raw data to usable heatmap format
  return data.map((point) => ({
    x: point.longitude,
    y: point.latitude,
    intensity: point.bandwidthUsage,
  }));
}
