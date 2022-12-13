# About this project

<ins>Overview</ins>

- Project for UIUC CS 222 Fall 2022, Group 21.
- An interactive website designed to inform readers about climate change and predictions of its evolution through a few graphical and machine learning models, as well as through various textual passages with important infromation about climate change.

<ins>Implementation details</ins>

- Frontend written in React, using Plotly to render plots and Axios as the frontend HTTP client.
- Backend written in Django, using Django REST API framework to handle HTTP requests.
- Eslint and Prettier used for linting and formatting.
- Sea level model uses data from https://datahub.io/core/sea-level-rise#readme to train a neural network model of several layers on global sea levels, using the Keras library to form the model object.
- Carbon dioxide vs temperatures model loaded data sets from Kaggle about land temperatures for major cities around the world as well as atmospheric carbon dioxide emissions over time. Boath datasets were loaded, cleaned, processed, and computed on in Pandas dataframes.

## <ins>Model Details and Roles</ins>

- Colin and Yifeng worked on the React frontend and the Django backend
- Aashi and Tianfen worked on the project models themselves, with Aashi working on the Carbon Dioxide-Temperatures model and Tianfan working on the predictive Sea Levels model

# Running The Project

<ins>[Configuring Eslint and Prettier](https://medium.com/how-to-react/config-eslint-and-prettier-in-visual-studio-code-for-react-js-development-97bb2236b31a)</ins>

- npm install eslint --save-dev
- npx eslint --init
- npm install eslint-config-prettier eslint-plugin-prettier prettier --save-dev
- npm i --save-dev enzyme
- npm i axios
- npm i --save-dev enzyme
- npm i react-icons
- npm install react-datepicker --save

<ins>Starting React and Django</ins>

- Create a new python virtual environment.
- Open two terminal windows.
- In the first:
  - Change directory into "backend" (`cd backend`), then activate the python virtual environment you created; assuming you named it "venv", the command is `source venv/bin/activate`.
  - Install all dependencies given in the requirements.txt file (`pip install -r requirements.txt`).
  - run the Django server (`python3 manage.py runserver`). The server should be hosted at https://localhost:8000.
- In the second:
  - change directory into "frontend" (`cd frontend`).
  - start the React app (`npm start`). The React app should be hosted at https://localhost:3000.
- Note: your dependencies may vary based on your machine, operating system, and date of use of the project. Be wary of this, and update dependencies (requirements.txt) as necessary.

[![Django CI](https://github.com/CS222-UIUC/course-project-group-21/actions/workflows/django.yml/badge.svg?branch=main)](https://github.com/CS222-UIUC/course-project-group-21/actions/workflows/django.yml)

# course-project-group-21

course-project-group-21 created by GitHub Classroom

https://docs.google.com/document/d/1KFKTAIavM3E1Q-zBtBCn4gfUPRWPpLpZz2lcftUBvko/edit#heading=h.qougbnz1fcec

## Github PR Steps Basics \n

1 - git chcekout main

2 -git pull origin main

3 - git checkout -b feature/<new_meaningful_verb>
