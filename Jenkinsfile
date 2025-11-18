pipeline {
    agent any

    environment {
        IMAGE_NAME = "sharath-food-truck"
        IMAGE_TAG  = "jenkins"
    }

    stages {
        stage('Checkout') {
            steps {
                // Gets code from Git (Jenkins will use your repo URL)
                checkout scm
            }
        }

        stage('Show Files') {
            steps {
                bat 'dir'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %IMAGE_NAME%:%IMAGE_TAG% ."
            }
        }

        // You can enable this later once you configure a registry
        stage('Post-Build') {
            steps {
                echo "Build completed. Image: ${env.IMAGE_NAME}:${env.IMAGE_TAG}"
            }
        }
    }
}
