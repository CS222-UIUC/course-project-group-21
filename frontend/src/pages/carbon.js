// import React, { Component } from 'react';
// import axios from 'axios';
// import Plot from 'react-plotly.js';


// export default class Carbon extends Component {
//   state = {
//     x: null,
//     y: null,
//   }

//   renderGraph = () => {
//     // get temp graph data from axios

//     axios({
//       method: 'get',
//       url: 'http://127.0.0.1:8000/carbon/',
//     })
//       .then((response) => {        
//         var dataframe = Object.values(JSON.parse(response.data.dataframe))

//         this.setState({
//           x: Object.keys(dataframe[0]),
//           y: Object.values(dataframe[0]),

//         })
//       })
//       .catch(error => {
//         console.error(error);
//     });

//       return (
//         <Plot
//           data = {[
//             {
//               x: this.state.x,
//               y: this.state.y,
//               type: 'scatter',
//               mode: 'markers',
//               name: 'Carbon Model',
//               marker: {color: 'blue'}
//             },
//           ]}
//           layout={{
//             title: 'Effect of Carbon Dioxide Level on Average Global Temperature',
//             xaxis: {
//               title: 'Carbon Dioxide (ppm)',
//             },
//             yaxis: {
//               title: 'Average Temperature'
//             },
//           }}
//         />
//       );
//     };

//     render() {
//       return (
//         <div>
//           <h1>
//             Carbon Model
//           </h1>
//           {this.renderGraph()}
//         </div>
//       );
//     }
// }

import React, { useEffect, useState } from 'react';

import axios from 'axios';
import Plot from 'react-plotly.js';
// import { parseISO, format } from 'date-fns';
// import xtype from 'xtypejs';


function Carbon() {
  // const [axes, setAxes] = useState(null);
  // const [tavgX, setTavgX] = useState(null);
  // const [tavgY, setTavgY] = useState(null);
  // const [tminX, setTminX] = useState(null);
  // const [tminY, setTminY] = useState(null);
  // const [tmaxX, setTmaxX] = useState(null);
  // const [tmaxY, setTmaxY] = useState(null);
  const [data, setData] = useState(null);
  // const [theLayout, setTheLayout] = useState(null);
  // const [plot, setPlot] = useState(null);




  useEffect(() => {
    // get temp graph data from axios

    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/carbon/',
    })
      .then((response) => {
        const axes = Object.values(JSON.parse(response.data.dataframe));
        const x = Object.keys(axes[0]);
        const y = Object.values(axes[0]);

        const data = [
          {
            x: x,
            y: y,
            type: 'scatter',
            mode: 'markers',
            name: 'Carbon Model',
            marker: { color: 'blue' }
          },
        ];



        setData(data);

        // var theLayout = {

        // };

        // setData(data);

        // var plot = <Plot
        //   data = {data}
        //   layout = {layout}
        // />;

        // setPlot(plot);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);



  // useEffect(() => {
  //   var layout = {
  //     title: 'Temperature Time Series In Specified Time Interval and Location',
  //     xaxis: {
  //       range: ['1980-01-01', '2020-12-31'],
  //       title: 'Date',
  //     },
  //     yaxis: {
  //       title: 'Temperature'
  //     },
  //   };

  //   if (data) {
  //     Plotly.newPlot('temp-plot', data, layout);
  //   }
  // }, [data]);

  // const layout = ;

  // function plotOrLoading(data) {
  //   if (!data) {
  //     return
  // <div>
  //   <i className="fa fa-spinner fa-spin fa-3x fa-fw"></i>
  //   <span className="sr-only">Loading...</span>
  //   <p>Loading graph...</p>
  // </div>
  //   }

  // }


  return (
    <div id="myDiv" className="colintest">
      <h1> Carbon Emissions and Temperature </h1>
      {data ?
        (
          <Plot
            data={data}
            layout={{
              title: 'Effect of Carbon Dioxide Level on Average Global Temperature',
              xaxis: {
                title: 'Carbon Dioxide (ppm)',
              },
              yaxis: {
                title: 'Average Temperature'
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
      }
      <p>
      This time series model demonstrates the positive and linear relationship between carbon emissions 
      and global temperatures 1958 to 2013 in the United States. It uses datasets of temperatures for 
      major cities around the world and atmospheric carbon dioxide emissions over time. 
      </p>
      <p>
      This model highlights the massive contribution human-produced carbon dioxide emissions have to accelerating climate change. 
      </p>
    </div>
  );
}

export default Carbon;

