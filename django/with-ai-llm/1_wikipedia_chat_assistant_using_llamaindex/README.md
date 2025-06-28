> ⚠️ **Warning:** This project is under active development. Features and documentation may change frequently.

<br /><br />

# Django Wikipedia Title Extractor

This Django project provides an API that extracts the 5 most relevant Wikipedia article titles from a user query using OpenAI, then queries Wikipedia via a ReAct Agent before generating a synthesized answer. The project is fully dockerized, so no local Python or Django installation is required.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Project](#running-the-project)
- [Docker Commands](#docker-commands)
- [List of Available Routes](#list-of-available-routes)

## Prerequisites
- **No local Python or Django installation required!**  
  The project is fully dockerized and can be run with only Docker and Docker Compose.
- Docker and Docker Compose
- Git
- **Environment Variables:**  
  - Rename `.env.example` to `.env` in the project root directory.
  - Open `.env` and set your [OpenAI API key](https://platform.openai.com/account/api-keys):
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## Setup
1. **Clone the repository:**
    ```
    git clone https://github.com/brice-tossim/python.git
    cd python/django/with-ai-llm/1_wikipedia_chat_assistant_using_llamaindex
    ```

## Running the Project
```bash
./docker.sh up
```
This command will build the Docker containers and start the application.  
The API will be available at `http://localhost:8000/api/chat/`.

## Docker Commands
| Command            | Description                  |
|--------------------|-----------------------------|
| ./docker.sh up     | Build and start containers  |
| ./docker.sh logs   | View container logs         |
| ./docker.sh down   | Stop containers             |

## List of Available Routes
| Route                                 | Method | Description           | Required Fields |
|---------------------------------------|--------|-----------------------|-----------------|
| `http://localhost:8000/api/chat/`     | POST   | Submit your query     | `query`         |
