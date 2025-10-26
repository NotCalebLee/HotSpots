import React from "react";
import "./About.css";
import profile_img from "../../assets/Heat-Map2.jpg";
const About = () => {
  return (
    <div id="about" className="about">
      <div className="about-title">
        <h1>Sample Data</h1>
      </div>
      <div className="about-sections">
        <div className="about-left">
          <p>Dartmouth Data</p>
          <img src={profile_img} alt="" />
        </div>
        <div className="about-right">
          <div className="about-para">
            <p>Hong Kong </p>
            <img src={profile_img} alt="" />
          </div>
        </div>
      </div>
      {/*
      <div className="about-achievements">
        <div className="about-achievement">
          <h1>2</h1>
          <p>YEARS OF EXPERIENCE</p>
        </div>
        <hr />
        <div className="about-achievement">
          <h1>HI</h1>
          <p>AND GOODBYE</p>
        </div>
        <hr />
        <div className="about-achievement">
          <h1>GO</h1>
          <p>AWAY</p>
        </div>
      </div>
*/}
    </div>
  );
};

export default About;
