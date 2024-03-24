# FastAPI Blogging Platform

## Overview
This blogging platform is a modern web application built with FastAPI and PostgreSQL. It provides a robust backend for managing user accounts and blog posts, supporting features like user registration, authentication, blog post creation, updating, and deletion. Designed with scalability and performance in mind, it leverages FastAPI's asynchronous request handling and PostgreSQL's reliable data storage capabilities.

## Setup and Execution Instructions
### Prerequisites
- Docker
- Docker Compose
### Getting Started
1. **Clone the Repository**

   ```bash
   git clone https://your-repository-url.git
   cd your-repository-directory
   ```
2. **Build and Run with Docker Compose**

   This command will build the FastAPI application and PostgreSQL services, then run them in containers.
   ```bash
    docker-compose up --build
    ```
    Access the application at http://localhost:8000 and the API documentation at http://localhost:8000/docs.
3. **Running Database Migrations**
   
   Migrations are automatically applied when the Docker container starts, thanks to the entrypoint.sh script. If you need to create new migrations, run:
     ```bash
    docker-compose exec web alembic revision --autogenerate -m "Your message"
    docker-compose exec web alembic upgrade head
    ```
### Stopping the Application

To stop the application and remove containers, networks, and volumes created by docker-compose up, run:
```bash
docker-compose down -v
 ```
### Architectural and Data Model Choices
#### Architecture
- FastAPI: Chosen for its high performance and ease of use for building RESTful APIs. FastAPI's support for asynchronous request handling allows the application to scale and handle large volumes of traffic efficiently.
- PostgreSQL: A robust and reliable relational database management system that provides advanced features and supports complex queries. It's used to store and manage user and blog post data securely.
- Docker and Docker Compose: Used for containerizing the application and its dependencies, ensuring consistency across different environments and simplifying deployment and scaling.
#### Data Model
- Users: Represented with a User model, including fields for id, email, hashed_password, name, and location. Users are authenticated using their email and password, with passwords securely hashed and stored.
- Blog Posts: The BlogPost model includes id, title, content, and owner_id fields. owner_id is a foreign key linking a blog post to its owner (a user), enforcing that only the creator of a blog post can edit or delete it.
#### Security
- Authentication: Utilizes OAuth2 with Password (and hashing), including JWT tokens for secure and stateless authentication.
- Password Hashing: Passwords are hashed using bcrypt, ensuring that plaintext passwords are never stored or transmitted.