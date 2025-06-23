# Django Simple CRUD REST API Project

This documentation provides instructions for setting up and running the project.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Project](#running-the-project)
- [Docker Commands](#docker-commands)
- [List of available routes](#list-of-available-routes)

## Prerequisites
- Docker and Docker Compose
- Git

## Setup
Clone the repository:
```bash
git clone https://github.com/bricioo/python.git
cd django_simple_crud_rest_api
```

## Running the Project
```bash
./docker.sh up
```
This command will build the Docker containers and start the application. The API will be available at `http://localhost:8000/api/courses/`.

## Docker Commands
| Command | Description |
|---------|-------------|
| ./docker.sh up | Build and start containers |
| ./docker.sh logs | View container logs |
| ./docker.sh down | Stop containers |
| ./docker.sh test | Run tests |

## List of available routes
| Route | Method | Description | Required Fields |
|-------|---------|-------------|-----------------|
| `http://localhost:8000/api/courses/` | GET | List all courses | None |
| `http://localhost:8000/api/courses/` | POST | Create new course | title, summary |
| `http://localhost:8000/api/courses/<id>/` | GET | Get course details | None |
| `http://localhost:8000/api/courses/<id>/` | PATCH | Update course | title, summary |
| `http://localhost:8000/api/courses/<id>/` | DELETE | Delete course | None |
