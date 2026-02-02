pipeline {
    agent any

    environment {
        KUBECONFIG = "/home/devipriya/.kube/config"
        IMAGE_NAME = "python-cicd-app"
        IMAGE_TAG = "${env.BRANCH_NAME}"      // Branch name used as Docker tag
        FULL_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning repository for branch ${env.BRANCH_NAME}..."
                checkout scm
            }
        }

        stage('Test Minikube Connection') {
            steps {
                sh 'kubectl get nodes'
            }
        }

        stage('Build Docker Image in Minikube') {
            steps {
                sh '''
                echo "Setting Docker environment to Minikube..."
                eval $(minikube -p minikube docker-env)

                echo "Building Docker image for branch ${BRANCH_NAME}..."
                docker build -t ${FULL_IMAGE} .

                echo "Verify Docker image exists in Minikube..."
                docker images | grep ${IMAGE_NAME}
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                echo "Deploying branch ${BRANCH_NAME} to Kubernetes..."

                # Replace the image in deployment.yaml dynamically
                sed -i "s|image: python-cicd-app:.*|image: ${FULL_IMAGE}|" k8s/deployment.yaml

                kubectl apply -f k8s/deployment.yaml
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'kubectl get pods'
            }
        }
    }

    post {
        success { echo "✅ Pipeline for branch ${BRANCH_NAME} completed successfully!" }
        failure { echo "❌ Pipeline for branch ${BRANCH_NAME} failed!" }
    }
}
