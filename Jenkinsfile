pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'paycare-etl'
    }
    
    stages {
        stage('Init') {
            stage('Clone Repository') {
                steps {
                    git 'https://github.com/littlerobinson/jenkins-etl-skeleton.git'
                }
            }
            stage('Install Dependencies') {
                steps {
                    sh 'pip install -r requirements.txt'
                }
            }
        }
        stage('Test') {
            stage('Run Unit Tests') {
                steps {
                    sh 'pytest --junitxml=unit-tests.xml'
                }
                post {
                    always {
                        junit 'unit-tests.xml'  // Publish test results
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
            }
        }
    }
}
