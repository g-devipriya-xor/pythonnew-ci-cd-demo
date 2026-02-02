pipeline {
    agent any

    environment {
        // Docker pointing to Minikube
        DOCKER_TLS_VERIFY = "1"
        DOCKER_HOST = "tcp://192.168.49.2:2376"
        DOCKER_CERT_PATH = "/var/lib/jenkins/.minikube/profiles/minikube"
        MINIKUBE_ACTIVE_DOCKERD = "minikube"

        // Kubernetes config for Jenkins
        KUBECONFIG = "/var/lib/jenkins/.kube/config"

        // Docker image info
        IMAGE_NAME = "python-cicd-app"
        IMAGE_TAG = "latest"
        FULL_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning repository..."
                git branch: 'main', url: 'https://github.com/g-devipriya-xor/pythonnew-ci-cd-demo.git'
            }
        }

        stage('Test Minikube Connection') {
            steps {
                sh '''
                set -e
                echo "Testing Docker connection to Minikube..."
                docker info | grep "Server Version"

                echo "Testing Kubernetes connection..."
                kubectl config view
                kubectl get nodes
                '''
            }
        }

        stage('Build Docker Image in Minikube') {
            steps {
                sh '''
                set -e
                echo "Building Docker image inside Minikube..."
                docker build -t ${FULL_IMAGE} .

                echo "Verify Docker image exists in Minikube..."
                docker images | grep ${IMAGE_NAME}
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                set -e
                echo "Applying Kubernetes manifests..."
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml

                echo "Waiting for deployment to complete..."
                kubectl rollout status deployment/${IMAGE_NAME}
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                set -e
                echo "Listing pods..."
                kubectl get pods

                echo "Checking service endpoints..."
                kubectl get svc
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline succeeded! Application deployed to Minikube."
        }
        failure {
            echo "❌ Pipeline failed! Check logs for details."
        }
    }
}
