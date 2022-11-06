import './TodoApp.css';

// For APIs
import 'semantic-ui-css/semantic.min.css';
import React, { Component } from "react";
import Modal from "./components/Modal";
import axios from 'axios';

class TodoApp extends Component {
  constructor(props) {
    super(props);
     
    // add the props here
    this.state = {
     
      // the viewCompleted prop represents the status
      // of the task. Set it to false by default
      viewCompleted: false,
      activeItem: {
        title: "",
        description: "",
        completed: false
      },
       
      // this list stores all the completed tasks
      taskList: []
    };
  }

  // This updates the TodoApp to get the latest information from the localhost API
  componentDidMount() {
    this.refreshList();
  }
  refreshList = () => {
    axios   //Axios to send and receive HTTP requests
      .get("http://localhost:8000/api/tasks/")
      .then(res => this.setState({ taskList: res.data }))
      .catch(err => console.log(err));
  };

  // This arrow function sets viewCompleted equal to the status parameter
  displayCompleted = status => {
    if (status) {
      return this.setState({ viewCompleted: true });
    }
    return this.setState({ viewCompleted: false });
  };

  // This function separates the list between complete tasks
  // and incomplete tasks
  renderTabList = () => {
    return (
      <div className="my-5 tab-list">
        <span
          onClick={() => this.displayCompleted(true)}
          // Display if the task is complete
          className={this.state.viewCompleted ? "active" : ""}
        >
          Completed
            </span>
        <span
          onClick={() => this.displayCompleted(false)}
          // Display if the task is incomplete
          className={this.state.viewCompleted ? "" : "active"}
        >
          Incompleted
            </span>
      </div>
    );
  };

  // Main variable to render items on the screen
  renderItems = () => {
    const { viewCompleted } = this.state;
    const newItems = this.state.taskList.filter(
      (item) => item.completed === viewCompleted
    );
    return newItems.map((item) => (
      <li
        key={item.id}
        className="list-group-item d-flex justify-content-between align-items-center"
      >
        <span
          className={`todo-title mr-2 ${
            this.state.viewCompleted ? "completed-todo" : ""
          }`}
          title={item.description}
        >
          {item.title}
        </span>
        <span>
          <button
            onClick={() => this.editItem(item)}
            className="btn btn-secondary mr-2"
          >
            Edit
          </button>
          <button
            onClick={() => this.handleDelete(item)}
            className="btn btn-danger"
          >
            Delete
          </button>
        </span>
      </li>
    ));
  };

  toggle = () => {
    //add this after modal creation
    this.setState({ modal: !this.state.modal });
  };
  // handleSubmit = (item) => {
  //   this.toggle();
  //   alert("save" + JSON.stringify(item));
  // };

  // Submit an item
  handleSubmit = (item) => {
    this.toggle();
    if (item.id) {
      // if old post to edit and submit
      axios
        .put(`http://localhost:8000/api/tasks/${item.id}/`, item)
        .then((res) => this.refreshList());
      return;
    }
    // if new post to submit
    axios
      .post("http://localhost:8000/api/tasks/", item)
      .then((res) => this.refreshList());
  };

  // Delete item
  handleDelete = (item) => {
    axios
      .delete(`http://localhost:8000/api/tasks/${item.id}/`)
      .then((res) => this.refreshList());
  };
  // handleDelete = (item) => {
  //   alert("delete" + JSON.stringify(item));
  // };

  // Create item
  createItem = () => {
    const item = { title: "", description: "", completed: false };
    this.setState({ activeItem: item, modal: !this.state.modal });
  };
 
  //Edit item
  editItem = (item) => {
    this.setState({ activeItem: item, modal: !this.state.modal });
  };
 
  // Start by visual effects to viewer
  render() {
    return (
      <main className="content">
        <h1 className="text-success text-uppercase text-center my-4">
          Task Manager
        </h1>
        <div className="row ">
          <div className="col-md-6 col-sm-10 mx-auto p-0">
            <div className="card p-3">
              <div className="">
                <button onClick={this.createItem} className="btn btn-info">
                  Add task
                </button>
              </div>
              {this.renderTabList()}
              <ul className="list-group list-group-flush">
                {this.renderItems()}
              </ul>
            </div>
          </div>
        </div>
        {this.state.modal ? (
          <Modal
            activeItem={this.state.activeItem}
            toggle={this.toggle}
            onSave={this.handleSubmit}
          />
        ) : null}
      </main>
    );
  }
}

export default TodoApp;
