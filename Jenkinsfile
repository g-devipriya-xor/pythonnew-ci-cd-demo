pipeline {
    agent any

    environment {
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

        stage('Build Docker Image inside Minikube VM') {
            steps {
                script {
                    sh """
                    echo "Building Docker image inside Minikube via SSH..."
                    minikube ssh '
                        cd /home/docker
                        mkdir -p python-ci
                    '

                    # Copy files from host to Minikube VM
                    minikube cp ./ /home/docker/python-ci

                    # SSH into Minikube and build Docker image
                    minikube ssh "
                        cd /home/docker/python-ci
                        docker build -t ${FULL_IMAGE} .
                        docker images | grep ${IMAGE_NAME}
                    "
                    """
                }
            }
        }

        stage('Deploy to Kubernetes inside Minikube VM') {
            steps {
                script {
                    sh """
                    echo "Deploying to Kubernetes via SSH..."
                    minikube ssh "
                        kubectl apply -f /home/docker/python-ci/deployment.yaml
                        kubectl apply -f /home/docker/python-ci/service.yaml
                        kubectl rollout status deployment/${IMAGE_NAME}
                        kubectl get pods
                        kubectl get svc
                    "
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully (via minikube ssh)!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs."
        }
    }
}
