#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${GREEN}>>> $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}>>> Error: $1${NC}"
}

# Build and start containers
build_and_up() {
    print_status "Building Docker images..."
    docker-compose build

    if [ $? -eq 0 ]; then
        print_status "Starting containers..."
        docker-compose up -d
        print_status "Containers are up and running!"
        print_status "API is available at http://localhost:8000"
        print_status "View logs with: ./docker.sh logs"
    else
        print_error "Build failed!"
        exit 1
    fi
}

# View logs
view_logs() {
    print_status "Showing logs..."
    docker-compose logs -f
}

# Stop containers
stop() {
    print_status "Stopping containers..."
    docker-compose down
}

# Run tests
run_tests() {
    print_status "Running tests..."
    docker-compose build && docker-compose run --rm wikipedia-chat-assistant pytest
}

# Main script
case "$1" in
    "up")
        build_and_up
        ;;
    "logs")
        view_logs
        ;;
    "down")
        stop
        ;;
    "test")
        run_tests
        ;;
    *)
        echo "Usage: ./docker.sh [command]"
        echo "Commands:"
        echo "  up    - Build and start containers"
        echo "  logs  - View container logs"
        echo "  down  - Stop containers"
        echo "  test  - Run tests"
        ;;
esac