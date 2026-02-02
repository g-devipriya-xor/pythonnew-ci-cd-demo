pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/g-devipriya-xor/pythonnew-ci-cd-demo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                # Point Docker to Minikube daemon
                eval $(minikube docker-env)
                
                # Disable TLS verification in Jenkins
                export DOCKER_TLS_VERIFY=""
                export DOCKER_CERT_PATH=""
                
                # Build the Docker image
                docker build -t python-cicd-app:latest .
                
                # Verify image exists in Minikube
                docker images | grep python-cicd-app
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                # Apply deployment YAML
                kubectl apply -f deployment.yaml
                
                # Wait for rollout
                kubectl rollout status deployment/python-cicd-app
                '''
            }
        }
    }

    post {
        success {
            echo "✅ App deployed successfully to Minikube!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs for errors."
        }
    }
}
