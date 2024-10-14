
# Social Media App Backend with FastAPI

This repository contains a backend for a social media app built using FastAPI. The app provides basic functionality for posts, user management, authentication, and voting.

## Features:

1. **Post Routes**  
   - Create, update, delete, and retrieve posts.
   
2. **User Routes**  
   - Create users and retrieve users by ID.
   
3. **Auth Routes**  
   - Manage login and authentication.
   
4. **Vote Routes**  
   - Upvote posts.

## Installation:

1- Clone the repository:
   ```bash
   git clone https://github.com/AliAfshar7/FastAPI.git
   cd FastAPI
```
2- Install dependencies:
``` bash
pip install fastapi[all]
```
3- Set up the PostgreSQL database and configure environment variables. Create a .env file in the project root with the following content:
``` bash 
DATABASE_HOSTNAME = localhost
DATABASE_PORT = 5432
DATABASE_PASSWORD = passward_that_you_set
DATABASE_NAME = name_of_database
DATABASE_USERNAME = User_name
SECRET_KEY = 09d25e094faa2556c818166b7a99f6f0f4c3b88e8d3e7 
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60(base)
```
4- Run the FASTAPI server
```bash
uvicorn app.main:app --reload 
```
## Database Setup:
* Ensure PostgreSQL is running.
* Create a database and configure the environment variables in the .env file
The server will start at http://127.0.0.1:8000.

## Technologies Used:
* **FastAPI**: For building APIs.
* **PostgreSQL**: For the database.
* **SQLAlchemy**: For database interaction.
* **Pydantic**: For data validation.
* **Alembic**: For database migrations.
* **Uvicorn**: ASGI server to run FastAPI.
* **pytest**: For testing the application.
* **Docker**: For containerizing the application.
* **GitHub Actions**: For CI/CD pipeline automation.


