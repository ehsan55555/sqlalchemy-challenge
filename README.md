# sqlalchemy-challenge

## This repository contains the code for the "SurfsUp" SQLAlchemy Challenge, focusing on analyzing weather data and creating a Flask API. Below, you'll find an overview of the contents of this repository and how to use them.

# Repository Structure
 --------------------
## - SurfsUp: 
 This directory contains the a folder called starter_code with the main code files for the challenge.

## - Resources: 
 This folder contains the data files used for analysis.

## - hawaii.sqlite: 
 The SQLite database file containing weather data.

## - climate_analysis.ipynb: 
 Jupyter Notebook where initial analysis and code development took place.

## - app.py: 
 Flask application script implementing the API routes.

## - README.md: 
 This document, providing an overview of the repository and instructions.

# Files and Purpose
 ------------------
## - climate_analysis.ipynb: 
 This Jupyter Notebook was used for initial data analysis and code development. It includes the process of connecting to the SQLite database, querying data, and performing exploratory analysis.

## - app.py: 
 This script contains the Flask application that serves as the API. It defines the various routes for retrieving weather and temperature data and provides them as JSON responses.

## - Resources/hawaii.sqlite: 
 This SQLite database file holds the weather data needed for analysis and API responses.

# Using the Flask API
 -------------------
 1. Clone or download this repository to your local machine.
 2. Navigate to the SurfsUp directory.
 3. Run the Flask app by executing the following command in your terminal:
 4. After the Flask app is running, open your web browser and navigate to http://127.0.0.1:5000/. You'll find a list of available routes and their descriptions.
 5. You can access the API routes by appending the desired route to the base URL (http://127.0.0.1:5000).

# Additional Information
 -----------------------
 The SurfsUp directory is organized to contain all the necessary code files for the challenge. The Flask app (app.py) defines routes for precipitation data, station information, temperature observations, and temperature statistics based on specified start and end dates.
