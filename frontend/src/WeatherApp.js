import './WeatherApp.css';

import { Dimmer, Loader } from 'semantic-ui-react';
import { useEffect, useState } from "react";
import Weather from './components/weather';

function WeatherApp() {

    const [lat, setLat] = useState([]);
    const [long, setLong] = useState([]);
    const [weatherData, setWeatherData] = useState([]);
  
    useEffect(() => {
      const fetchWeatherData = async () => {
        navigator.geolocation.getCurrentPosition(function(position) {
          setLat(position.coords.latitude);
          setLong(position.coords.longitude);
        });
  
        await fetch(`${process.env.REACT_APP_API_URL}/weather/?lat=${lat}&lon=${long}&units=metric&APPID=${process.env.REACT_APP_API_KEY}`)
        .then(res => res.json())
        .then(result => {
          setWeatherData(result)
        });
      }
      fetchWeatherData();
    }, [lat,long])
  
    return (
      <div className="App">
  
        {(typeof weatherData.main != 'undefined') ? (
          <Weather weatherData={weatherData}/>
        ): (
          <div>
            <Dimmer active>
              <Loader>Weather Data Loading..</Loader>
            </Dimmer>
        </div>
        )}
      </div>
    );
  }

  export default WeatherApp;