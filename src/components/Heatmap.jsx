import React, { useEffect, useRef } from "react";

export default function Heatmap({ data }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!data || data.length === 0) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    data.forEach((point) => {
      const radius = Math.min(50, point.intensity / 10);
      const gradient = ctx.createRadialGradient(point.x, point.y, 0, point.x, point.y, radius);
      gradient.addColorStop(0, "rgba(255, 0, 0, 0.8)");
      gradient.addColorStop(1, "rgba(255, 0, 0, 0)");

      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(point.x, point.y, radius, 0, Math.PI * 2);
      ctx.fill();
    });
  }, [data]);

  return <canvas id="heatmap" ref={canvasRef}></canvas>;
}
