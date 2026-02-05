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
                echo "Cloning repository for branch ${BRANCH_NAME}..."
                git branch: "${BRANCH_NAME}", url: 'https://github.com/g-devipriya-xor/pythonnew-ci-cd-demo.git'
            }
        }
	stage('Save Build Info') {
            steps {
                sh '''
                echo "Build for branch ${BRANCH_NAME} started at $(date)" > result.log
                echo "Repository: https://github.com/g-devipriya-xor/pythonnew-ci-cd-demo" >> result.log
                echo "Docker image to be built: ${IMAGE_NAME}:${BRANCH_NAME}" >> result.log
                '''
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
		# Generate a random NodePort between 30010-32767
		NODE_PORT=$(shuf -i 30010-32767 -n 1)
		echo "Using NodePort: $NODE_PORT"

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
            echo " Pipeline for branch ${BRANCH_NAME} completed successfully!"
	    emailext (
		to: "${NOTIFY_EMAIL}",
                subject: "Build Success: ${JOB_NAME} [${BRANCH_NAME}]",
                body: """
                Good news! The Jenkins pipeline for branch ${BRANCH_NAME} completed successfully.
                Check build details: ${BUILD_URL} ${BUILD_URL}
                """
            )
        }
        failure {
            echo " Pipeline for branch ${BRANCH_NAME} failed!"
	    emailext (
		 to: "${NOTIFY_EMAIL}",
                subject: "Build Failed: ${JOB_NAME} [${BRANCH_NAME}]",
                body: """
                Oops! The Jenkins pipeline for branch ${BRANCH_NAME} failed.
                Please check the console output:${BUILD_URL} ${BUILD_URL}
                """
            )
        }
    }
}
