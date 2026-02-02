pipeline {
    agent any

    environment {
        // Kubernetes config for Jenkins
        KUBECONFIG = "/home/devipriya/.kube/config"

        // Docker image info
        IMAGE_NAME = "python-cicd-app"
        IMAGE_TAG = "${env.BRANCH_NAME ?: 'main'}" // Use branch name or main if null
        FULL_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning repository for branch ${env.BRANCH_NAME}..."
                git branch: "${env.BRANCH_NAME}", url: 'https://github.com/g-devipriya-xor/pythonnew-ci-cd-demo.git'
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
                echo "Deploying branch ${BRANCH_NAME} to Kubernetes..."

                # Assign NodePort per branch
                case "${BRANCH_NAME}" in
                  main) NODE_PORT=30001 ;;
                  feature1) NODE_PORT=30002 ;;
                  feature2) NODE_PORT=30003 ;;
                  *) NODE_PORT=30010 ;;
                esac

                # Replace placeholders in deployment.yaml
                sed -i "s|image: python-cicd-app:.*|image: ${FULL_IMAGE}|g" k8s/deployment.yaml
                sed -i "s|PLACEHOLDER_NODEPORT|${NODE_PORT}|g" k8s/deployment.yaml

                # Apply Kubernetes deployment
                kubectl apply -f k8s/deployment.yaml
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                echo "Checking pods for branch ${BRANCH_NAME}..."
                kubectl get pods -l app=python-cicd-app
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline for branch ${BRANCH_NAME} completed successfully!"
        }
        failure {
            echo "❌ Pipeline for branch ${BRANCH_NAME} failed!"
        }
    }
}
