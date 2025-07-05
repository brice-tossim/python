pipeline {
    agent any

    environment {
        // Define environment variables
        DOCKER_IMAGE = "django-wikipedia-chat-assistant"
        DOCKER_TAG = "latest"
    }

    stages {
        stage("Checkout") {
            steps {
                // Jenkins automatically checks out the code
                echo "Code checkout out from GitHub"
            }
        }

        stage("Build") {
            steps {
                echo "Running Django tests..."
                // Use your existing test script
                sh "cd django/with-ai-llm/1_wikipedia_chat_assistant_using_llamaindex && ./docker.sh test"
            }
        }

        stage("Build Docker Image") {
            steps {
                script {
                    echo "Building Docker image..."
                    sh "cd django/with-ai-llm/1_wikipedia_chat_assistant_using_llamaindex && docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline completed!"
            // Clean up containers
            sh "docker system prune -f"
        }
        success {
            echo "Pipeline succeeded!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}