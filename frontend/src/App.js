import './App.css';

// For APIs
import 'semantic-ui-css/semantic.min.css';
import { Dimmer, Loader } from 'semantic-ui-react';
import React, { useEffect, useState } from "react";
import Weather from './components/weather';
import Todo from './components/todo';
import axios from 'axios'; 

// class TodoApp extends Component {
//   constructor(props) {
//     super(props);
     
//     // add the props here
//     this.state = {
     
//       // the viewCompleted prop represents the status
//       // of the task. Set it to false by default
//       viewCompleted: false,
//       activeItem: {
//         title: "",
//         description: "",
//         completed: false
//       },
       
//       // this list stores all the completed tasks
//       taskList: []
//     };
//   }

//   // Add componentDidMount()
//   componentDidMount() {
//     this.refreshList();
//   }

//   refreshList = () => {
//     axios   //Axios to send and receive HTTP requests
//       .get("http://localhost:8000/api/tasks/")
//       .then(res => this.setState({ taskList: res.data }))
//       .catch(err => console.log(err));
//   };

//   // this arrow function takes status as a parameter
//   // and changes the status of viewCompleted to true
//   // if the status is true, else changes it to false
//   displayCompleted = status => {
//     if (status) {
//       return this.setState({ viewCompleted: true });
//     }
//     return this.setState({ viewCompleted: false });
//   };

//   // this array function renders two spans that help control
//   // the set of items to be displayed(ie, completed or incomplete)
//   renderTabList = () => {
//     return (
//       <div className="my-5 tab-list">
//         <span
//           onClick={() => this.displayCompleted(true)}
//           className={this.state.viewCompleted ? "active" : ""}
//         >
//           completed
//             </span>
//         <span
//           onClick={() => this.displayCompleted(false)}
//           className={this.state.viewCompleted ? "" : "active"}
//         >
//           Incompleted
//             </span>
//       </div>
//     );
//   };

//   // Main variable to render items on the screen
//   renderItems = () => {
//     const { viewCompleted } = this.state;
//     const newItems = this.state.taskList.filter(
//       (item) => item.completed === viewCompleted
//     );
//     return newItems.map((item) => (
//       <li
//         key={item.id}
//         className="list-group-item d-flex justify-content-between align-items-center"
//       >
//         <span
//           className={`todo-title mr-2 ${
//             this.state.viewCompleted ? "completed-todo" : ""
//           }`}
//           title={item.description}
//         >
//           {item.title}
//         </span>
//         <span>
//           <button
//             onClick={() => this.editItem(item)}
//             className="btn btn-secondary mr-2"
//           >
//             Edit
//           </button>
//           <button
//             onClick={() => this.handleDelete(item)}
//             className="btn btn-danger"
//           >
//             Delete
//           </button>
//         </span>
//       </li>
//     ));
//   };

//   toggle = () => {
//     //add this after modal creation
//     this.setState({ modal: !this.state.modal });
//   };
//   handleSubmit = (item) => {
//     this.toggle();
//     alert("save" + JSON.stringify(item));
//   };

//   // Submit an item
//   handleSubmit = (item) => {
//     this.toggle();
//     if (item.id) {
//       // if old post to edit and submit
//       axios
//         .put(`http://localhost:8000/api/tasks/${item.id}/`, item)
//         .then((res) => this.refreshList());
//       return;
//     }
//     // if new post to submit
//     axios
//       .post("http://localhost:8000/api/tasks/", item)
//       .then((res) => this.refreshList());
//   };

//   // Delete item
//   handleDelete = (item) => {
//     axios
//       .delete(`http://localhost:8000/api/tasks/${item.id}/`)
//       .then((res) => this.refreshList());
//   };
//   handleDelete = (item) => {
//     alert("delete" + JSON.stringify(item));
//   };
// }

function App() {

  const [lat, setLat] = useState([]);
  const [long, setLong] = useState([]);
  const [weatherData, setWeatherData] = useState([]);
  const [tData, setTodoData] = useState([]);

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
    const fetchTodoData = async () => {
      await axios.get(`${process.env.TODO_LIST_API_URL}/1`)
      .then(res => setTodoData( res.data ))
    }
    fetchWeatherData();
    fetchTodoData();
  }, [lat,long,tData])

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
    <Todo todoData={tData}/>
    </div>
  );
}

export default App;
