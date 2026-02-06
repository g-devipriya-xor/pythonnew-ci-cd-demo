pipeline {
    agent any

    environment {
        KUBECONFIG = "/home/devipriya/.kube/config"
        IMAGE_NAME = "python-cicd-app"
        NOTIFY_EMAIL = "G.Devipriya@Xoriant.Com"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning repository for branch ${env.BRANCH_NAME}..."
                checkout scm
            }
        }

        stage('Save Build Info') {
            steps {
                script {
                    def tagName = env.BRANCH_NAME ?: "PR-${env.CHANGE_ID}"
                    sh """
                    echo "Build for branch ${tagName} started at $(date)" > result.log
                    echo "Repository: https://github.com/g-devipriya-xor/pythonnew-ci-cd-demo" >> result.log
                    echo "Docker image to be built: ${IMAGE_NAME}:${tagName}" >> result.log
                    """
                }
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
                script {
                    def tagName = env.BRANCH_NAME ?: "PR-${env.CHANGE_ID}"
                    sh """
                    echo "Setting Docker environment to Minikube..."
                    eval \$(minikube -p minikube docker-env)

                    echo "Building Docker image inside Minikube..."
                    docker build -t ${IMAGE_NAME}:${tagName} .

                    echo "Verify Docker image exists in Minikube..."
                    docker images | grep ${IMAGE_NAME}
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                anyOf {
                    branch 'main'
                    expression { env.BRANCH_NAME != null } // deploy for both main and PRs
                }
            }
            steps {
                script {
                    def tagName = env.BRANCH_NAME ?: "PR-${env.CHANGE_ID}"
                    sh """
                    echo "Deploying branch ${tagName} to Kubernetes..."
                    NODE_PORT=\$(shuf -i 30010-32767 -n 1)
                    echo "Using NodePort: \$NODE_PORT"

                    sed -i "s|PLACEHOLDER_TAG|${tagName}|g" k8s/deployment.yaml
                    sed -i "s|PLACEHOLDER_NODEPORT|\$NODE_PORT|g" k8s/deployment.yaml

                    # Delete existing service (ignore if not exists)
                    kubectl delete service ${IMAGE_NAME}-service-${tagName} || true

                    # Apply Deployment & Service
                    kubectl apply -f k8s/deployment.yaml

                    # Force rollout restart
                    kubectl rollout restart deploy/${IMAGE_NAME}-${tagName}
                    """
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    def tagName = env.BRANCH_NAME ?: "PR-${env.CHANGE_ID}"
                    sh """
                    echo "Checking pods for branch ${tagName}..."
                    kubectl get pods -l app=${IMAGE_NAME}-${tagName} -o wide
                    """
                }
            }
        }

        stage('Archive Artifacts') {
            steps {
                echo "Archiving build artifacts..."
                archiveArtifacts artifacts: 'app.py,k8s/*.yaml,result.log', fingerprint: true
            }
        }

        stage('Cleanup PR Deployments') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                echo "Cleaning up PR deployments after merge..."

                for DEPLOY in $(kubectl get deploy -o name | grep ${IMAGE_NAME}- | grep -v main); do
                    echo "Deleting deployment $DEPLOY"
                    kubectl delete $DEPLOY
                done

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
            echo "Pipeline for branch ${env.BRANCH_NAME ?: 'PR-${env.CHANGE_ID}'} completed successfully!"
            emailext(
                to: "${NOTIFY_EMAIL}",
                subject: "Build Success: ${JOB_NAME} [${env.BRANCH_NAME ?: 'PR-${env.CHANGE_ID}'}]",
                body: """
                Good news! The Jenkins pipeline for branch ${env.BRANCH_NAME ?: 'PR-${env.CHANGE_ID}'} completed successfully.
                Check build details: ${BUILD_URL}
                """
            )
        }
        failure {
            echo "Pipeline for branch ${env.BRANCH_NAME ?: 'PR-${env.CHANGE_ID}'} failed!"
            emailext(
                to: "${NOTIFY_EMAIL}",
                subject: "Build Failed: ${JOB_NAME} [${env.BRANCH_NAME ?: 'PR-${env.CHANGE_ID}'}]",
                body: """
                Oops! The Jenkins pipeline for branch ${env.BRANCH_NAME ?: 'PR-${env.CHANGE_ID}'} failed.
                Please check the console output: ${BUILD_URL}
                """
            )
        }
    }
}
