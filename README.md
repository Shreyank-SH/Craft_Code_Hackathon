# Craft Code Hackathon

This project is designed for the Craft Code Hackathon and includes a Python-based application that automates the detection and classification of issues using machine learning techniques and integrated auditing systems.

## Project Overview

The application is built to analyze images, handle auditing tasks, and manage employee data. It integrates a database system and offers functionality for users and managers to upload images, detect whether the image represents a serious issue, and manage other related tasks.

## Key Components

### 1. `app.py`
The main application script that initializes and runs the server. It integrates all the other components and handles requests from users and managers for image processing, auditing, and database management.

### 2. `employee.py`
This module is responsible for handling employee-related functionalities. Employees can upload images, raise issues, and interact with the auditing system through this module.

### 3. `gemini_solution.py`
Contains the solution for detecting issues from images. The AI model analyzes the uploaded images and classifies them based on predefined labels like "serious" or "not serious".

### 4. `login_system.py`
Handles the authentication system. This module allows users to log in and manage their accounts in a secure manner.

### 5. `manager.py`
The manager's dashboard, where all raised issues are displayed. Managers can review the issues, look at the uploaded images, and check the suggested solutions provided by the AI.

### 6. `setup_db.py`
A script to initialize and configure the database (`auditing.db`). It contains the structure and schema definitions necessary for setting up the auditing system and storing employee/manager data.

### 7. `auditing.db`
The SQLite database used by the application to store employee, issue, and audit data.

### 8. `requirements.txt`
A list of dependencies required to run the project. You can install all necessary Python libraries by running:

## Usage

- **Employees:** Employees can upload images through the employee dashboard, which will be processed by the AI model to detect issues.
- **Managers:** Managers can log in to the manager's dashboard and review issues raised by employees. They can view the AI-suggested solutions and take appropriate action.

## AI Image Analysis

The image analysis functionality is powered by a machine learning model integrated into `gemini_solution.py`. It utilizes pre-trained models to analyze uploaded images and detect whether they represent a serious issue or not.
