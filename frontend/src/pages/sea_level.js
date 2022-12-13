// eslint-disable-next-line no-unused-vars

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

function Sea() {
  const cur_date = new Date()
  const [data, setData] = useState(null);
  const [startDate, setStartDate] = useState(new Date(2022, 11, 12)); // month is 0-indexed; "0" is "January"
  const [futureMonth, setfutureMonth] = useState(cur_date.getMonth());
  const [futureYear, setfutureYear] = useState(cur_date.getFullYear());
  const [invalidDate, setInvalidDate] = useState(false);
  // const [dateChanged, setdateChanged] = useState(true);
  const [graphLoading, setGraphLoading] = useState(true)

  function changeDate(date) {
    setStartDate(date)
    setfutureYear(date.getFullYear())
    setfutureMonth(date.getMonth())
  }

  useEffect(() => {
    // get temp graph data from axios
    setGraphLoading(true);

    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/sealevel/',
      data: {
        year: futureYear,
        month: futureMonth,
        // day: this.state.startDate.getDate(),
      }
    })
      .then((response) => {
        // const actual = Object.values(JSON.parse(response.data.actual));
        const predicted = Object.values(JSON.parse(response.data.predicted));
        console.log("got here 7")

        // const actualX = Object.keys(actual[0]);
        // const actualY = Object.values(actual[0]);

        const predictedX = Object.keys(predicted[0]);
        const predictedY = Object.values(predicted[0]);

        const data = [
          // {
          //   x: actualX,
          //   y: actualY,
          //   name: 'Actual Sea Level',
          //   type: 'scatter',
          //   mode: 'lines+markers',
          //   marker: { color: 'red' }
          // },
          {
            x: predictedX,
            y: predictedY,
            name: 'Predicted sea level',
            type: 'scatter',
            mode: 'lines+markers',
            marker: { color: 'blue' }
          },
        ];


        setData(data);
        setGraphLoading(false);
        // setdateChanged(false);
      })
      .catch(error => {
        console.error(error);
      });
  }, [startDate]);



  return (
    <div id="myDiv" className="colintest">
      <h1> Sea Level Predictions </h1>
      {graphLoading ?
        (
          <div>
          <i className="fa fa-spinner fa-spin fa-3x fa-fw"></i>
          <span className="sr-only">Loading...</span>
          <p>Loading graph...</p>
        </div>
        ) :
        (
          <Plot
            data={data}
            layout={{
              title: 'Prediction of Sea Levels up to Selected Future Date',
              xaxis: {
                title: 'Months Elapsed Since Selected Month',
              },
              yaxis: {
                title: 'GMSL (mm)'
              },
            }}
          />
        )
      }

      <div>
        <p>Select the date of the month in the future you would like to predict sea levels for.</p>
        <DatePicker selected={startDate} onChange={
          (date:Date) => 
          {
            const cur_date = new Date();
            const cur_month = cur_date.getMonth();
            const cur_year = cur_date.getFullYear();
            const future_month = date.getMonth();
            const future_year = date.getFullYear();
            var months_into_future = (future_year - cur_year) * 12 + (future_month - cur_month);
            if (months_into_future < 0) {
              setInvalidDate(true);
            } else {
              setInvalidDate(false);
              changeDate(date);
              useEffect();
            }
          }
        } />
        <div>
          {invalidDate? 
            (
              <p>You entered a date in the past. Please enter a date in the future.</p>
            ) :
            (
              <p>Check out the changed graph!</p>
            )

          }
        </div>
      </div>


      <div>
        <p>
          For the design of the sea level prediction model, we used a time-series model with a neural network of several layers, shown below.
        </p>
        <p>
          With this model, we are trying to predict global cumulative sea-level changes since 1901, based on a combination of long-term tide
          gauge measurements and recent satellite measurements, with data retrieved from <a href={"https://datahub.io/core/sea-level-rise#readme"}>https://datahub.io/core/sea-level-rise#readme</a>
          . It shows
          average absolute sea level change, which refers to the height of the ocean surface, regardless of whether nearby land is rising or
          falling. Here, the 0 sea level is the sea level on 06/15/1990. The functionality of this model is to receive an input value representing
          the months from now and returns a prediction with a plot of future sea level changes until then.
        </p>
        <p>
          While the majority of Americans believe the government isn&apos;t doing enough to protect the environment, climate change is still a
          divisive, ideological issue.
        </p>
        <p>
          From the output plot of this figure, we can see the upward trend of sea level rise. The rising speed in the near future, as shown in
          the plot, should be reckoned with. Many coastal cities have already been impacted by the flooding, not to mention those wildlife
          habitats. In addition, soil and groundwater are also affected by the sea level rise, leading to a world that is no longer salubrious
          to human and animal life.
        </p>
        <p>
          To fight against the threats brought by sea level rise, we need to cut our carbon footprint and protect natural structures as much as
          possible. Sea level rise is an essential topic in climate change and will impact everyone’s daily life. We are responsible for trying
          our best to fight against that to protect the environment.
        </p>
      </div>
    </div>
  );
}

export default Sea;

