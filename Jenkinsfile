pipeline {

    agent any

    environment {
        DOCKER_USER = "shiwanishinedocker"
        K3S_SERVER = "52.4.197.67"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/Shiwani-Yaduka/studysync-ai.git'
            }
        }

        stage('Build Backend Image') {
            steps {
                sh '''
                docker build \
                -t $DOCKER_USER/studysync-backend:latest \
                -f docker/backend.Dockerfile .
                '''
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh '''
                docker build \
                -t $DOCKER_USER/studysync-frontend:latest \
                -f docker/frontend.Dockerfile .
                '''
            }
        }

        stage('Push Images') {
            steps {

                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USERNAME',
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {

                    sh '''
                    echo $DOCKER_PASSWORD | docker login \
                    -u $DOCKER_USERNAME --password-stdin
                    '''

                    sh '''
                    docker push $DOCKER_USER/studysync-backend:latest
                    '''

                    sh '''
                    docker push $DOCKER_USER/studysync-frontend:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {

                sh '''
                ssh ubuntu@$K3S_SERVER \
                'KUBECONFIG=$HOME/.kube/config kubectl rollout restart deployment studysync-backend'
                '''

                sh '''
                ssh ubuntu@$K3S_SERVER \
                'KUBECONFIG=$HOME/.kube/config kubectl rollout restart deployment studysync-frontend'
                '''
            }
        }
    }
}