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

        stage('Build Docker Image in Minikube') {
            steps {
                script {
                    sh '''
                    echo "Switching Docker CLI to Minikube..."
                    eval $(minikube -p minikube docker-env)

                    echo "Building Docker image..."
                    docker build -t ${FULL_IMAGE} .

                    echo "Verifying image exists in Minikube..."
                    docker images | grep ${IMAGE_NAME}
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Use Jenkins Secret Text credential for kubeconfig
                withCredentials([string(credentialsId: 'kubeconfig-minikube', variable: 'KUBECONFIG_CONTENT')]) {
                    sh '''
                    echo "Creating temporary kubeconfig..."
                    echo "$KUBECONFIG_CONTENT" > kubeconfig.yaml
                    export KUBECONFIG=$(pwd)/kubeconfig.yaml

                    echo "Applying Kubernetes manifests..."
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml

                    echo "Waiting for deployment rollout..."
                    kubectl rollout status deployment/${IMAGE_NAME}

                    echo "Verifying pods and services..."
                    kubectl get pods
                    kubectl get svc
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed. Check the logs for details."
        }
    }
}
