import React from "react";
import survey from "../images/PewSurvey.png"

// yifeng wrote content
const Beliefs = () => {
  return (
    <div>
      <div className="colintest">
        <div>
          <h1>
            <span style={{ fontWeight: 'bold' }}>
              American Beliefs About Climate Change
            </span>
          </h1>
          <p>
            Most Americans say that the federal government isn&apos;t doing enough to protect the environment, regardless of benefits to humans or the nature.
            They believe that the United States should focus on developing alternative sources of fuel instead of expanding the use of fossil fuels.
          </p>
          <p>
            However, Democrats and Republicans are split over the government&apos;s handling of climate change.
            90% of Democrats believe the government is doing too little, while just under 40% of Republicans believe the same.
            Similarly, Moderates/Liberals believe the government isn&apos;t doing enough, while few Conservatives say the same.
            Age also has a negative correlation to concern for the climate.
          </p>
          <p>
            While the majority of Americans believe the government isn&apos;t doing enough to protect the environment, climate change is still a divisive, ideological issue.
          </p>
        </div>
        <div>
          <img src={survey} alt="Survey done by Pew Research Center" />
        </div>
        <p>References:</p>
        <p>
            <a href={"https://www.pewresearch.org/science/2019/11/25/u-s-public-views-on-climate-and-energy/"}>https://www.pewresearch.org/science/2019/11/25/u-s-public-views-on-climate-and-energy/</a>
        </p>
      </div>
    </div >
  );
};

export default Beliefs;