pipeline {
  agent any

  environment {
    IMAGE = "YOUR_DOCKERHUB_USERNAME/sharath-food-truck"
    TAG = "${env.BUILD_NUMBER ?: 'latest'}"
    DOCKERHUB_CRED = "dockerhub-creds" // configure in Jenkins
    KUBECONFIG_CRED = "kubeconfig"      // optional: for kubectl deploy
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Unit Test') {
      steps {
        // optional: run basic python lint/tests
        sh 'python3 -m pip install -r requirements.txt'
        sh 'python3 -m pyflakes app.py || true' // pyflakes optional; install pyflakes if you want
      }
    }

    stage('Build Docker Image') {
      steps {
        sh "docker build -t ${IMAGE}:${TAG} ."
      }
    }

    stage('Vulnerability Scan (Trivy)') {
      steps {
        // Optional step: requires trivy installed on agent
        sh 'trivy image --severity HIGH,CRITICAL --exit-code 1 ${IMAGE}:${TAG} || true'
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: DOCKERHUB_CRED, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
          sh "docker push ${IMAGE}:${TAG}"
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        // Option A: use kubectl configured on agent (kubeconfig credential)
        withCredentials([file(credentialsId: KUBECONFIG_CRED, variable: 'KUBECONFIG_FILE')]) {
          sh 'mkdir -p $HOME/.kube'
          sh 'cp $KUBECONFIG_FILE $HOME/.kube/config'
          sh "kubectl set image deployment/sharath-food-truck sharath-food-truck=${IMAGE}:${TAG} --record || kubectl apply -f k8s/"
        }
      }
    }
  }

  post {
    always {
      sh 'docker images || true'
    }
  }
}
