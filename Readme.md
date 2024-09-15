Flask Chat Application with Docker and MongoDB
Overview
This project is a Flask-based chat application with a backend integrated with MongoDB. It features user management, a question-answering system, and Docker-based containerization. Users can interact with the chat system through a web UI and are managed based on their interaction frequency.

Table of Contents
Features
Prerequisites
Setup and Installation
Running the Application
API Endpoints
Docker Setup
Debugging
Contributing
License
Features
User management with frequency control.
Chat interface to interact with the bot.
Question-answering system using LangChain and Google Generative AI.
MongoDB integration for storing user data and queries.
Dockerized setup for easy deployment.
Prerequisites
Before setting up the project, ensure you have the following installed:

Docker
Docker Compose
Python 3.10
Pip
Setup and Installation
Clone the Repository

bash
Copy code
git clone https://github.com/your-username/your-repository.git
cd your-repository
Create a .env File

Create a .env file in the root directory of the project with the following content:

env
Copy code
FLASK_ENV=development
MONGO_URI=mongodb://mongo:27017/mydatabase
Replace mydatabase with your desired database name.
Ensure the .env file is not included in version control (it is excluded by .dockerignore).
Install Dependencies

Although Docker will handle this, you can manually install dependencies in a virtual environment if needed:

bash
Copy code
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Running the Application
Build and Start Docker Containers

Build and start the containers using Docker Compose:

bash
Copy code
docker-compose up --build
This will build the Docker image for the Flask app and start both the app and MongoDB services.

Access the Application

Open your web browser and go to http://localhost:5000 to access the chat interface.
API Endpoints
/ask: Submit a query to the chat system.

Method: POST
Request Body: { "user_id": "<user_id>", "question": "<question>", "top_k": <top_k>, "threshold": <threshold> }
Response: JSON object with answers and source documents.
/user: Retrieve the latest top 5 queries for a user.

Method: POST
Request Body: { "user_id": "<user_id>" }
Response: JSON object with the latest queries and timestamps.
/health: Check if the API is active.

Method: GET
Response: Random response for health check.
/search: Search for top results based on prompt text.

Method: POST
Request Body: { "text": "<text>", "top_k": <top_k>, "threshold": <threshold> }
Response: List of top results with similarity scores.
Docker Setup
Dockerfile: Defines the Python environment and application setup.
docker-compose.yml: Configures services for Flask and MongoDB.
.dockerignore: Specifies files to exclude from the Docker image build context.
Building and Running Docker Containers
Build Docker Image

bash
Copy code
docker build -t your_image_name .
Run Docker Compose

bash
Copy code
docker-compose up
This will start both the Flask application and MongoDB.

Debugging
If you encounter issues, follow these debugging steps:

Check Docker Logs

View logs for the Flask application:

bash
Copy code
docker-compose logs app
View logs for MongoDB:

bash
Copy code
docker-compose logs mongo
Verify Environment Variables

Ensure that the .env file is correctly configured and contains the proper MongoDB URI.

Check MongoDB Connection

Verify that MongoDB is running and accessible. Use the MongoDB shell or a GUI tool to connect to the database:

bash
Copy code
mongo mongodb://localhost:27017/mydatabase
Inspect Container File System

Access the running container to check file existence and configurations:

bash
Copy code
docker exec -it <container_id> /bin/bash
Debug Flask Application

Add debug print statements or use a debugger to trace issues within your Flask application. Ensure FLASK_ENV is set to development for detailed error messages.