pipeline {
    agent any


    environment {
        VENV = "venv"
        REMOTE_USER = "ubuntu"
        REMOTE_HOST = "3.111.171.3"
        REMOTE_DIR = "/home/ubuntu/flask_practice"
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

                mkdir -p ~/.ssh
                ssh-keyscan -H $REMOTE_HOST >> ~/.ssh/known_hosts 2>/dev/null || true

                ssh $REMOTE_USER@$REMOTE_HOST "
                    if [ -d $REMOTE_DIR/.git ]; then
                        cd $REMOTE_DIR &&
                        git fetch origin main &&
                        git reset --hard origin/main
                    else
                        git clone -b main https://github.com/rajkumarsaw22/flask_practice.git $REMOTE_DIR
                    fi &&
                    cd $REMOTE_DIR &&
                    python3 -m venv venv &&
                    . venv/bin/activate &&
                    pip install --upgrade pip &&
                    pip install -r requirements.txt &&
                    pkill -f app.py || true &&
                    nohup ./venv/bin/python app.py > app.log 2>&1 &
                "
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