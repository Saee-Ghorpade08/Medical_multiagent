
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out Medical Healthcare Assistant project'
                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                bat 'python --version'
                bat 'pip --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m pytest tests/ -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t medical-healthcare-assistant:latest .'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the console output for errors.'
        }

        always {
            echo 'Jenkins pipeline execution finished.'
        }
    }
}
