pipeline {
    agent any

    environment {
        IMAGE = "sharathwork99/sharath-food-truck"
        TAG   = "jenkins"
    }

    stages {

        stage('Checkout') {
            steps {
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
                bat "docker build -t %IMAGE%:%TAG% ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                    usernameVariable: 'USER', passwordVariable: 'PASS')]) {

                    bat "echo %PASS% | docker login -u %USER% --password-stdin"
                    bat "docker push %IMAGE%:%TAG%"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                echo Applying manifests...
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                kubectl apply -f k8s/ingress.yaml

                echo Restarting deployment...
                kubectl rollout restart deployment/foodtruck-deployment

                echo Waiting for rollout...
                kubectl rollout status deployment/foodtruck-deployment
                '''
            }
        }
    }
}
