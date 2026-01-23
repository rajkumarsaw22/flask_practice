pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
            args '-u root'
        }
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python --version
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Code Quality - Black') {
            steps {
                sh 'black --check .'
            }
        }

        stage('Static Analysis - Pylint') {
            steps {
                sh 'pylint app.py || true'
            }
        }

        stage('Security Scan - Bandit') {
            steps {
                sh 'bandit -r . || true'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'pytest tests/'
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    echo "Deploying Flask app to staging..."
                    nohup python app.py > app.log 2>&1 &
                '''
            }
        }
    }

    post {
        success {
            script {
                try {
                    emailext(
                        subject: "SUCCESS: Jenkins Build ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: "Build, tests, and deployment completed successfully.",
                        to: "rajkumar22.tech@gmail.com"
                    )
                } catch (err) {
                    echo "Email notification failed, but build succeeded."
                }
            }
        }

        failure {
            script {
                try {
                    emailext(
                        subject: "FAILURE: Jenkins Build ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: "Pipeline failed. Please check Jenkins logs.",
                        to: "rajkumar22.tech@gmail.com"
                    )
                } catch (err) {
                    echo "Email notification failed."
                }
            }
        }
    }
}
