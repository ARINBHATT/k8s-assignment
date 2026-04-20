pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-k8s-app"
        IMAGE_TAG  = "v${BUILD_NUMBER}"
    }

    stages {

        stage('Clone Repository') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes...'
                sh "kubectl set image deployment/nginx-deployment nginx=${IMAGE_NAME}:${IMAGE_TAG}"
                echo 'Image updated successfully!'
            }
        }

        stage('Verify Deployment') {
            steps {
                echo 'Verifying...'
                sh "kubectl get pods"
                sh "kubectl get deployments"
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded! Deployed ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}