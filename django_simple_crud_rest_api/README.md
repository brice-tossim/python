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
| `{{BASE_URL}}/api/courses/` | GET | List all courses | None |
| `{{BASE_URL}}/api/courses/` | POST | Create new course | title, summary |
| `{{BASE_URL}}/api/courses/<id>/` | GET | Get course details | None |
| `{{BASE_URL}}/api/courses/<id>/` | PATCH | Update course | title, summary |
| `{{BASE_URL}}/api/courses/<id>/` | DELETE | Delete course | None |
