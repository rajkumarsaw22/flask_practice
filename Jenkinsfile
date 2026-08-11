pipeline {
    agent any

    environment {
        VENV = "venv"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/rajkumarsaw22/flask_practice.git'
            }
        }

        stage('Build') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                . venv/bin/activate
                pytest
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                echo "Deploying application to staging environment..."
                pkill -f app.py || true
                nohup ./venv/bin/python app.py > app.log 2>&1 &
                '''
            }
        }
    }

    post {
        success {
            mail to: 'rajkumar22.libra@gmail.com',
                 subject: "SUCCESS: Jenkins Build #${BUILD_NUMBER}",
                 body: "Build completed successfully."
        }

        failure {
            mail to: 'rajkumar22.libra@gmail.com',
                 subject: "FAILED: Jenkins Build #${BUILD_NUMBER}",
                 body: "Build failed. Check Jenkins console output."
        }
    }
}