pipeline {
    agent any

    stages {

        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Git Clone') {
            steps {
                echo 'Checking out repository...'
                git branch: 'main', url: 'https://github.com/aneeshravikumar2002-eng/dev-1.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                sh '''
                pip install -r requirements.txt
                pip install pytest pytest-cov
                '''
            }
        }

        stage('Run Tests & Coverage') {
            steps {
                echo 'Running unit tests...'
                sh '''
                pytest --cov=. --cov-report=xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('My SonarQube Server') {
                        sh """
                        ${scannerHome}/bin/sonar-scanner \
                        -Dsonar.projectKey=news-app \
                        -Dsonar.projectName=news-app \
                        -Dsonar.sources=. \
                        -Dsonar.python.coverage.reportPaths=coverage.xml
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh '''
                docker build -t aneesh292002/news-app:${BUILD_NUMBER} \
                -t aneesh292002/news-app:latest .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-login',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_PASS'
                )]) {
                    sh '''
                    echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
                    docker push aneesh292002/news-app:${BUILD_NUMBER}
                    docker push aneesh292002/news-app:latest
                    docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes...'
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh '''
                    kubectl --kubeconfig=$KUBECONFIG apply -f k8s/deployment.yml
                    kubectl --kubeconfig=$KUBECONFIG apply -f k8s/service.yml
                    kubectl --kubeconfig=$KUBECONFIG rollout status deployment/news
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Build failed. Keeping Docker artifacts for debugging.'
        }
    }
}
