pipeline {
    agent any

    environment {
        ECR_URI = "159750416379.dkr.ecr.us-east-1.amazonaws.com/python-cicd-app"
    }

    stages {

        stage('Checkout') {
            steps {
                // Pull code from GitHub
                git credentialsId: 'git-creds', url: 'https://github.com/yourusername/pythonnew-ci-cd-demo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build the Docker image on EC2 using sudo
                sh "sudo docker build -t python-cicd-app:latest ."
            }
        }

        stage('Login to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                    // Authenticate to AWS ECR
                    sh 'aws ecr get-login-password --region us-east-1 | sudo docker login --username AWS --password-stdin $ECR_URI'
                }
            }
        }

        stage('Push to ECR') {
            steps {
                // Tag and push the Docker image to ECR
                sh "sudo docker tag python-cicd-app:latest $ECR_URI:latest"
                sh "sudo docker push $ECR_URI:latest"
            }
        }
    }

    post {
        success {
            echo "Docker image successfully pushed to ECR!"
        }
        failure {
            echo "Pipeline failed. Check logs for errors."
        }
    }
}
