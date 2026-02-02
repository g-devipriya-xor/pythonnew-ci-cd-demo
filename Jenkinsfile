pipeline {
    agent any

    environment {
        KUBECONFIG = "/home/devipriya/.kube/config"
        IMAGE_NAME = "python-cicd-app"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning repository for branch ${BRANCH_NAME}..."
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

                echo "Building Docker image inside Minikube..."
                docker build -t ${IMAGE_NAME}:${BRANCH_NAME} .

                echo "Verify Docker image exists in Minikube..."
                docker images | grep ${IMAGE_NAME}
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                echo "Deploying branch ${BRANCH_NAME} to Kubernetes..."

                # Assign unique NodePort per branch
                if [ "$BRANCH_NAME" = "main" ]; then
                  NODE_PORT=30001
                elif [ "$BRANCH_NAME" = "feature1" ]; then
                  NODE_PORT=30002
                elif [ "$BRANCH_NAME" = "feature2" ]; then
                  NODE_PORT=30003
                else
                  NODE_PORT=30010  # fallback port for new branches or PRs
                fi

                # Replace placeholders in deployment.yaml
                sed -i "s|PLACEHOLDER_TAG|${BRANCH_NAME}|g" k8s/deployment.yaml
                sed -i "s|PLACEHOLDER_NODEPORT|$NODE_PORT|g" k8s/deployment.yaml

                # Delete existing branch-specific Service (ignore error if not exists)
                kubectl delete service ${IMAGE_NAME}-service-${BRANCH_NAME} || true

                # Apply Deployment & Service
                kubectl apply -f k8s/deployment.yaml

                # Force rollout restart to pick up new image/code
                kubectl rollout restart deploy/${IMAGE_NAME}-${BRANCH_NAME}
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                echo "Checking pods for branch ${BRANCH_NAME}..."
                kubectl get pods -l app=${IMAGE_NAME}-${BRANCH_NAME} -o wide
                '''
            }
        }

        stage('Cleanup PR Deployments') {
            when {
                branch 'main'  // Run only on main after merge
            }
            steps {
                sh '''
                echo "Cleaning up PR deployments after merge..."

                # Delete PR-specific deployments
                for DEPLOY in $(kubectl get deploy -o name | grep ${IMAGE_NAME}- | grep -v main); do
                    echo "Deleting deployment $DEPLOY"
                    kubectl delete $DEPLOY
                done

                # Delete PR-specific services
                for SERVICE in $(kubectl get svc -o name | grep ${IMAGE_NAME}-service- | grep -v main); do
                    echo "Deleting service $SERVICE"
                    kubectl delete $SERVICE
                done
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
