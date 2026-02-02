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
                // Use Minikube's Docker daemon directly (no TLS issues)
                sh '''
                eval $(minikube docker-env --shell bash)
                docker build -t python-cicd-app:latest .
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh "kubectl apply -f deployment.yaml"
                sh "kubectl rollout status deployment/python-cicd-app"
            }
        }
    }

    post {
        success {
            echo "App deployed successfully to Minikube!"
        }
        failure {
            echo "Pipeline failed. Check logs."
        }
    }
}
