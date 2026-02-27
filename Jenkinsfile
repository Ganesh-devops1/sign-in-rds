pipeline {
    agent any

    environment {
        IMAGE_NAME = "signup-app"
        ECR_REPO = "YOUR-ACCOUNT-ID.dkr.ecr.ap-south-1.amazonaws.com/signup-app"
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/YOUR-USERNAME/signup-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Tag Image') {
            steps {
                sh 'docker tag $IMAGE_NAME:latest $ECR_REPO:latest'
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region ap-south-1 | \
                docker login --username AWS --password-stdin YOUR-ACCOUNT-ID.dkr.ecr.ap-south-1.amazonaws.com
                docker push $ECR_REPO:latest
                '''
            }
        }
    }
}