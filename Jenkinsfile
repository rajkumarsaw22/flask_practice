pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
        }
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                    python --version
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    pytest tests/
                '''
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
                        body: "Build succeeded and application deployed to staging.",
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
                        body: "Build failed. Please check Jenkins console output.",
                        to: "rajkumar22.tech@gmail.com"
                    )
                } catch (err) {
                    echo "Email notification failed."
                }
            }
        }
    }
}

