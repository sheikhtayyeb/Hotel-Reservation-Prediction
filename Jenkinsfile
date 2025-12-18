
pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages{

        stage('Cloning github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins ... ... ...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/sheikhtayyeb/Hotel-Reservation-Prediction.git']])
                }
            }
        }

         stage('Setting up our virtual env and installing dependencies'){
            steps{
                script{
                    echo 'Setting up our virtual env and installing dependencies ... ... ...'
                    sh '''
                    python  -m venv ${VENV_DIR} 
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                    }
                }
            }
     }
}