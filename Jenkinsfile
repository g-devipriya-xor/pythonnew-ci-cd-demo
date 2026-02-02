pipeline {
    agent any

    environment {
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
                echo "Testing Kubernetes connection..."
                kubectl get nodes
                '''
            }
        }

        stage('Build Docker Image in Minikube') {
            steps {
                sh '''
                echo "Setting Docker environment to Minikube..."
                eval $(minikube -p minikube docker-env)

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
