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
                // Build Docker image inside Minikube
                sh """
                    eval \$(minikube docker-env)
                    docker build -t python-cicd-app:latest .
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Deploy YAML should have containerPort: 5001
                sh "kubectl apply -f deployment.yaml"
                
                // Wait for rollout to complete
                sh "kubectl rollout status deployment/python-cicd-app"
            }
        }
    }

    post {
        success {
            echo "App deployed successfully to Minikube on port 5001!"
        }
        failure {
            echo "Pipeline failed. Check logs."
        }
    }
}
