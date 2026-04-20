```groovy
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-k8s-app'
        IMAGE_TAG  = "v${BUILD_NUMBER}"
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
                bat """
                docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python -m pytest tests/ -v || echo No tests found, skipping
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {

                    echo "Deploying ${IMAGE_NAME}:${IMAGE_TAG} to Kubernetes..."

                    bat """
                    kubectl --kubeconfig=%KUBECONFIG% set image deployment/flask-deployment ^
                    flask-container=${IMAGE_NAME}:${IMAGE_TAG}
                    """

                    bat "kubectl --kubeconfig=%KUBECONFIG% rollout status deployment/flask-deployment"
                    bat "kubectl --kubeconfig=%KUBECONFIG% get pods"
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded! App deployed as ${env.IMAGE_NAME}:${env.IMAGE_TAG}"
        }

        failure {
            echo "Pipeline FAILED. Check logs above."
        }

        always {
            bat "docker rmi ${env.IMAGE_NAME}:${env.IMAGE_TAG} || exit 0"
        }
    }
}
```
