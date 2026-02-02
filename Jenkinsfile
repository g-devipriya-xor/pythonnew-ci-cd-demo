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
                # Point Docker CLI to Minikube's Docker daemon
                eval $(minikube docker-env)

                # Build the Docker image
                docker build -t python-cicd-app:latest .

                # Optional: verify image exists in Minikube
                docker images | grep python-cicd-app
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                # Apply Kubernetes deployment
                kubectl apply -f deployment.yaml

                # Wait until rollout completes
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
            echo "❌ Pipeline failed. Check logs."
        }
    }
}

