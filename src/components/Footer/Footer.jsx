import React from "react";
import "./Footer.css";

const Footer = () => {
  return (
    <footer id="contact" className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <div className="footer-logo">
            <span className="footer-logo-icon">🔥</span>
            <span className="footer-logo-text">HotSpots</span>
          </div>
          <p className="footer-description">
            Interactive heatmap visualization for network usage in real-time.
            Discover hotspots and optimize your network experience.
          </p>
        </div>

        <div className="footer-section">
          <h3>Quick Links</h3>
          <ul className="footer-links">
            <li><a href="#home">Home</a></li>
            <li><a href="#about">Sample Data</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </div>

        <div className="footer-section">
          <h3>Connect</h3>
          <div className="footer-social">
            <a href="#" className="social-link">GitHub</a>
            <a href="#" className="social-link">Twitter</a>
            <a href="#" className="social-link">LinkedIn</a>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <div className="footer-divider"></div>
        <p className="footer-copyright">
          © 2024 HotSpots. All rights reserved. | Built with ❤️
        </p>
      </div>
    </footer>
  );
};

export default Footer;

