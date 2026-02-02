pipeline {
    agent any

    environment {
        // Let Jenkins know where kubeconfig is
        KUBECONFIG = "${env.HOME}/.kube/config"
        IMAGE_NAME = "python-cicd-app"
        IMAGE_TAG = "latest"
        FULL_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/g-devipriya-xor/pythonnew-ci-cd-demo.git'
            }
        }

        stage('Build Docker Image in Minikube') {
            steps {
                script {
                    // Use the same shell for docker-env and docker build
                    sh '''
                    echo "Using Minikube Docker daemon..."
                    eval $(minikube -p minikube docker-env)

                    echo "Building Docker image..."
                    docker build -t ${FULL_IMAGE} .

                    echo "Verifying image in Minikube..."
                    docker images | grep ${IMAGE_NAME}
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh '''
                    echo "Applying Kubernetes manifests..."
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml

                    echo "Waiting for deployment rollout..."
                    kubectl rollout status deployment/${IMAGE_NAME}
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                echo "Listing pods and services..."
                kubectl get pods
                kubectl get svc
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs."
        }
    }
}
