pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'paycare-etl'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/littlerobinson/jenkins-etl-skeleton.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'docker run --rm ${DOCKER_IMAGE} bash -c "pip install -r requirements.txt"'
            }
        }


        stage('Run Unit Tests') {
            steps {
                sh '''
                    docker run --rm \
                        -e PYTHONPATH=/app \
                        -v /tmp:/app
                        ${DOCKER_IMAGE} \
                        bash -c "pytest --junitxml=/tmp/unit-tests.xml"
                '''
            }
            post {
                always {
                    junit 'tmp/unit-tests.xml'
                }
            }
        }



        stage('Run Docker Container') {
            steps {
                script {
                    // Create input data file dynamically
                    sh 'echo "employee_id,employee_name,salary\n101,Alice,5000\n102,Bob,7000" > input_data.csv'

                    // Run the Docker container with mounted input/output files
                    sh 'docker run --rm -v $(pwd)/input_data.csv:/app/input_data.csv -v $(pwd)/output_data.csv:/app/output_data.csv ${DOCKER_IMAGE}'
                }
            }
        }
    }

    post {
        always {
            // Clean up workspace and remove dangling Docker images
            sh 'docker system prune -f'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
    }
}
