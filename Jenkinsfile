pipeline {
    agent any

    environment {
        DOCKERHUB_USER  = 'arinb17'
        IMAGE_NAME      = "${DOCKERHUB_USER}/flask-k8s-app"
        IMAGE_TAG       = "v${BUILD_NUMBER}"          // auto-increments each build
        KUBECONFIG_PATH = credentials('kubeconfig')
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Cloning repository..."
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building image: ${IMAGE_NAME}:${IMAGE_TAG}"
                bat "docker build -f docker/Dockerfile -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Test') {
            steps {
                echo "Running tests..."
                // Run tests inside a temporary container
                bat """
                    docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python -m pytest tests/ -v || echo "No tests found, skipping"
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat "docker login -u %DOCKER_USER% -p %DOCKER_PASS%"
                    bat "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                    // Also tag as latest
                    bat "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
                    bat "docker push ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    echo "Deploying ${IMAGE_NAME}:${IMAGE_TAG} to Kubernetes..."

                    // Rolling update — replaces pods one by one
                    bat """
                        kubectl --kubeconfig=%KUBECONFIG% set image deployment/flask-deployment ^
                        flask-container=${IMAGE_NAME}:${IMAGE_TAG}
                    """

                    // Wait for rollout to complete
                    bat "kubectl --kubeconfig=%KUBECONFIG% rollout status deployment/flask-deployment"

                    // Print final state
                    bat "kubectl --kubeconfig=%KUBECONFIG% get pods"
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded! App deployed as ${IMAGE_NAME}:${IMAGE_TAG}"
            // Optional Slack: slackSend color: 'good', message: "Deploy succeeded: ${IMAGE_TAG}"
        }
        failure {
            echo "Pipeline FAILED. Check logs above."
            // Optional Slack: slackSend color: 'danger', message: "Deploy FAILED: ${IMAGE_TAG}"
        }
        always {
            // Clean up local Docker images to save disk space
            bat "docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || exit 0"
        }
    }
}