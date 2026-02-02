pipeline {
    agent any

    environment {
        KUBECONFIG = "/home/devipriya/.kube/config"
        IMAGE_NAME = "python-cicd-app"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Cloning repository..."
                git branch: "${BRANCH_NAME}", url: 'https://github.com/g-devipriya-xor/pythonnew-ci-cd-demo.git'
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

                # For PRs, tag the image differently
                if [[ "$BRANCH_NAME" == PR-* ]]; then
                    IMAGE_TAG=${BRANCH_NAME}
                else
                    IMAGE_TAG=${BRANCH_NAME}
                fi

                echo "Building Docker image inside Minikube..."
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

                echo "Verify Docker image exists in Minikube..."
                docker images | grep ${IMAGE_NAME}
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                echo "Deploying ${BRANCH_NAME} to Kubernetes..."

                # Assign unique NodePort per branch or PR
                case "$BRANCH_NAME" in
                    main) NODE_PORT=30001 ;;
                    feature1) NODE_PORT=30002 ;;
                    feature2) NODE_PORT=30003 ;;
                    PR-*) NODE_PORT=$((30010 + ${BRANCH_NUMBER})) ;; # PR number ensures unique port
                    *) NODE_PORT=30100 ;; # fallback
                esac

                # Replace placeholders in deployment.yaml
                sed -i "s|PLACEHOLDER_TAG|${BRANCH_NAME}|g" k8s/deployment.yaml
                sed -i "s|PLACEHOLDER_NODEPORT|$NODE_PORT|g" k8s/deployment.yaml

                # Delete old service if exists
                kubectl delete service ${IMAGE_NAME}-service-${BRANCH_NAME} || true

                # Apply deployment & service
                kubectl apply -f k8s/deployment.yaml

                # Force rollout restart to ensure updated code runs
                kubectl rollout restart deploy/python-cicd-app-${BRANCH_NAME}
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                echo "Checking pods for ${BRANCH_NAME}..."
                kubectl get pods -l app=${IMAGE_NAME}-${BRANCH_NAME} -o wide
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline for ${BRANCH_NAME} completed successfully!"
        }
        failure {
            echo "❌ Pipeline for ${BRANCH_NAME} failed!"
        }
        cleanup {
            script {
                // Optional: delete PR deployments after testing
                if (BRANCH_NAME.startsWith("PR-")) {
                    sh "kubectl delete deploy python-cicd-app-${BRANCH_NAME} || true"
                    sh "kubectl delete service ${IMAGE_NAME}-service-${BRANCH_NAME} || true"
                }
            }
        }
    }
}
