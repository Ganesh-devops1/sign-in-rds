pipeline {
    agent any

    environment {
        IMAGE_NAME = "signup-app"
        ECR_REPO = "YOUR-ACCOUNT-ID.dkr.ecr.ap-south-1.amazonaws.com/signup-app"
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/Ganesh-devops1/sign-in-rds.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Push to ECR') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'aws-creds',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {

                    sh '''
                    export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                    export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

                    aws ecr get-login-password --region ap-south-1 | \
                    docker login --username AWS --password-stdin YOUR-ACCOUNT-ID.dkr.ecr.ap-south-1.amazonaws.com

                    docker tag $IMAGE_NAME:latest $ECR_REPO:latest
                    docker push $ECR_REPO:latest
                    '''
                }
            }
        }
    }
}
