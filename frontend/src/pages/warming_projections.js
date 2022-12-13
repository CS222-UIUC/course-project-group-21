import React, { useEffect, /*useState*/ } from 'react';
// import axios from 'axios';
// import Plot from 'react-plotly.js';
import projection from "../images/Climate Change Projections.png"


// yifeng wrote content
function Temperatures() {
  // const [data, setData] = useState(null);

  useEffect(() => {
    // axios({
    //   method: 'get',
    //   url: 'http://127.0.0.1:8000/temperatures/',
    // })
    //   .then((response) => {
    //     const axes = Object.values(JSON.parse(response.data.selected));
    //     const tavgXUnix = Object.keys(axes[0]);
    //     const tavgX = tavgXUnix.map(tElem => new Date(parseInt(tElem)));
    //     const tavgY = Object.values(axes[0]);


    //     const tminXUnix = Object.keys(axes[1]);
    //     const tminX = tminXUnix.map(tElem => new Date(parseInt(tElem)));
    //     const tminY = Object.values(axes[1]);

    //     const tmaxXUnix = Object.keys(axes[2]);
    //     const tmaxX = tmaxXUnix.map(tElem => new Date(parseInt(tElem)));
    //     const tmaxY = Object.values(axes[2]);

    //     const data = [
    //       {
    //         x: tmaxX,
    //         y: tmaxY,
    //         type: 'scatter',
    //         mode: 'lines+markers',
    //         name: 'tmax',
    //         marker: { color: 'green' }
    //       },
    //       {
    //         x: tavgX,
    //         y: tavgY,
    //         type: 'scatter',
    //         mode: 'lines+markers',
    //         name: 'tavg',
    //         marker: { color: 'blue' }
    //       },
    //       {
    //         x: tminX,
    //         y: tminY,
    //         type: 'scatter',
    //         mode: 'lines+markers',
    //         name: 'tmin',
    //         marker: { color: 'orange' }
    //       }
    //     ];
    //     setData(data);
    //   })
    //   .catch(error => {
    //     console.error(error);
    //   });
  }, []);



  return (
    <div id="myDiv" className="colintesttwo">
      {/* {data ?
        (
          <Plot
            data={data}
            layout={{
              title: 'Temperature Time Series In Specified Time Interval and Location',
              xaxis: {
                range: ['1980-01-01', '2020-12-31'],
                title: 'Date',
              },
              yaxis: {
                title: 'Temperature'
              },
            }}
          />
        ) :
        (
          <div>
            <i className="fa fa-spinner fa-spin fa-3x fa-fw"></i>
            <span className="sr-only">Loading...</span>
            <p>Loading graph...</p>
          </div>
        )
      } */}
          <div className="d-flex justify-content-center">
      <div>
        <h1>
          Projections of Global Temperatures
        </h1>
      </div>
      <p>
        There is a large disrepancy between current policies, current pledges, and current targets.
      </p>
      <div>
        <img src={projection} alt="Climate Change Projections"/>
      </div>
      <p>
        Given the current handling of climate change, it will result in average temperatures rising between 2.6-2.9 degrees Celsius above pre-industrial levels.
        The current 2030 targets expect temperatures to rise by 2.4 degrees Celsius, while the most optimistic projections resulted in around 1.8 degrees of warming.
        Greenhouse gases must be significantly reduced in the 2020s and 2030s in order to achieve an average warming of 1.5 degrees Celsius by 2100.
      </p>
      <h4>Reference:</h4>
      <a href={"https://climateactiontracker.org/global/temperatures/#:~:text=Current%20policies%20presently%20in%20place,C%20above%20pre-industrial%20levels."}>https://climateactiontracker.org/global/temperatures/#:~:text=Current%20policies%20presently%20in%20place,C%20above%20pre-industrial%20levels.</a>
    </div>
    </div>
  );


}

export default Temperatures;

