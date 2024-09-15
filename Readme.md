# Flask Chat Application with Docker and MongoDB

## Overview
This project is a Flask-based chat application with a backend integrated with MongoDB. It features user management, a question-answering system, and Docker-based containerization. Users can interact with the chat system through a web UI and are managed based on their interaction frequency.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Docker Setup](#docker-setup)
- [Debugging](#debugging)

## Features
- User management with frequency control
- Chat interface to interact with the bot
- Question-answering system using LangChain and Google Generative AI
- MongoDB integration for storing user data and queries
- Dockerized setup for easy deployment

## Prerequisites
Before setting up the project, ensure you have the following installed:
- Docker
- Docker Compose
- Python 3.10
- Pip

## Setup and Installation

### Clone the Repository
```bash
git clone https://github.com/soumyajit9979/21BRS1608_ML.git
cd your-repository
```

### Create a .env File
Create a `.env` file in the root directory of the project with the following content:
```
FLASK_ENV=development
MONGO_URI=mongodb://mongo:27017/mydatabase
```
Replace `mydatabase` with your desired database name.

**Note:** Ensure the `.env` file is not included in version control (it is excluded by `.dockerignore`).

### Install Dependencies
Although Docker will handle this, you can manually install dependencies in a virtual environment if needed:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Application

### Build and Start Docker Containers
Build and start the containers using Docker Compose:
```bash
docker-compose up --build
```
This will build the Docker image for the Flask app and start both the app and MongoDB services.

### Access the Application
Open your web browser and go to `http://localhost:5000` to access the chat interface.

## API Endpoints

- `/ask`: Submit a query to the chat system.
  - Method: POST
  - Request Body: `{ "user_id": "<user_id>", "question": "<question>", "top_k": <top_k>, "threshold": <threshold> }`
  - Response: JSON object with answers and source documents.
  - The default values for top_K is set to 5 and threshold is set to 0.5

- `/user`: Retrieve the latest top 5 queries for a user.
  - Method: POST
  - Request Body: `{ "user_id": "<user_id>" }`
  - Response: JSON object with the latest queries and timestamps.

- `/health`: Check if the API is active.
  - Method: GET
  - Response: Random response for health check.

- `/search`: Search for top results based on prompt text.
  - Method: POST
  - Request Body: `{ "text": "<text>", "top_k": <top_k>, "threshold": <threshold> }`
  - Response: List of top results with similarity scores.

## Docker Setup
- `Dockerfile`: Defines the Python environment and application setup.
- `docker-compose.yml`: Configures services for Flask and MongoDB.
- `.dockerignore`: Specifies files to exclude from the Docker image build context.

### Building and Running Docker Containers

#### Build Docker Image
```bash
docker build -t your_image_name .
```

#### Run Docker Compose
```bash
docker-compose up
```
**Note:** If you want to give your own personal Document, you can make the changes in line 30 of retiever.py and add path to you corresponding document, once done you are good to go for composing the docker file
This will start both the Flask application and MongoDB.

## Debugging
If you encounter issues, follow these debugging steps:

### Check Docker Logs
View logs for the Flask application:
```bash
docker-compose logs app
```

View logs for MongoDB:
```bash
docker-compose logs mongo
```

### Verify Environment Variables
Ensure that the `.env` file is correctly configured and contains the proper MongoDB URI.

### Check MongoDB Connection
Verify that MongoDB is running and accessible. Use the MongoDB shell or a GUI tool to connect to the database:
```bash
mongo mongodb://localhost:27017/mydatabase
```

### Inspect Container File System
Access the running container to check file existence and configurations:
```bash
docker exec -it <container_id> /bin/bash
```

### Debug Flask Application
Add debug print statements or use a debugger to trace issues within your Flask application. Ensure `FLASK_ENV` is set to `development` for detailed error messages.


![image](https://github.com/user-attachments/assets/52578427-a94b-47e2-ae22-e983e6e85522)


![image](https://github.com/user-attachments/assets/d8b4bc2b-c25a-4e10-a539-393b773e9aab)


![image](https://github.com/user-attachments/assets/67ebf785-462d-4644-b517-3b5c3ba08e61)


![image](https://github.com/user-attachments/assets/46509336-9dd7-42b4-b301-87ea05e2a6d6)


![image](https://github.com/user-attachments/assets/f5c787c3-234c-4b69-994c-91024a456ddf)

![image](https://github.com/user-attachments/assets/ef99a50d-2694-4f2e-a64c-eb484341afdf)


**Note**: Symantic Caching can be done, to store the response to any question in cache memory, which can be quickly responded when any query similar to it is asked once again, this reduces the use of LLM and helps us getting the response sooner as well
