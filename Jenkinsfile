pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"
<<<<<<< HEAD
        ACCOUNT_ID = "137452617596"
=======
        ACCOUNT_ID = "YOUR-AWS-ACCOUNT-ID"
>>>>>>> eb64fef (five commit)
        IMAGE_NAME = "sign-in-rds"
        ECR_REPO = "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                echo "Building Docker Image..."
                sh 'docker build -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Authenticate to ECR') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'aws-creds',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {

                    sh '''
                    export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                    export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                    export AWS_DEFAULT_REGION=$AWS_REGION

                    aws ecr get-login-password --region $AWS_REGION | \
                    docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                    '''
                }
            }
        }

        stage('Tag Docker Image') {
            steps {
                echo "Tagging Docker Image..."
                sh 'docker tag ${IMAGE_NAME}:latest ${ECR_REPO}:latest'
            }
        }

        stage('Push Image to ECR') {
            steps {
                echo "Pushing Image to ECR..."
                sh 'docker push ${ECR_REPO}:latest'
            }
        }
    }

    post {
        success {
            echo "Build & Push Completed Successfully 🚀"
        }
        failure {
            echo "Pipeline Failed ❌ Check Console Output"
        }
    }
<<<<<<< HEAD
}
=======
}
>>>>>>> eb64fef (five commit)
