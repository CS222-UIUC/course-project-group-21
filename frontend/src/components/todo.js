import React from 'react';
import './styles.css';

const TodoCard = ({todoData}) => (
    <div className="main">
        
        <div className="top">
            <p className="header">Todo: {todoData.title}</p>
        </div>

        <div className="flex">
            <p className="day">Description:</p>
        </div>

        <div className="flex">
            <p className="temp">{todoData.description}</p>
        </div>

        <div className="flex">
            <p className="sunrise-sunset">Completed: {todoData.completed}</p>
      </div>
    </div>
)

// Example usage for weatherData
{/* <Card>
    <Card.Content>
        <Card.Header className="header">{weatherData.name}</Card.Header>

        <p>{moment().format('dddd')}, {moment().format('LL')}</p>
        
        <p>Temprature: {weatherData.main.temp} &deg;C</p>
        <p>Sunrise: {new Date(weatherData.sys.sunrise * 1000).toLocaleTimeString('en-IN')}</p>
        <p>Sunset: {new Date(weatherData.sys.sunset * 1000).toLocaleTimeString('en-IN')}</p>
        <p>Description: {weatherData.weather[0].main}</p>
        <p>Humidity: {weatherData.main.humidity} %</p>
    </Card.Content>
  </Card> */}

export default TodoCard;