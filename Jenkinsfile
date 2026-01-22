pipeline {
    agent any

    environment {
        VENV = "${WORKSPACE}/venv"
    }

    stages {
        stage('Build') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh './venv/bin/pytest tests/'
            }
        }

        stage('Deploy') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sh '''
                echo "Deploying Flask app to staging..."
                # Example: run with gunicorn
                ./venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 app:app --daemon
                '''
            }
        }
    }

    post {
        success {
            emailext(
                subject: "SUCCESS: Jenkins Build ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "The build succeeded! Deployed to staging.",
                to: "your-email@example.com"
            )
        }
        failure {
            emailext(
                subject: "FAILURE: Jenkins Build ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "The build failed. Please check Jenkins logs.",
                to: "your-email@example.com"
            )
        }
    }
}
