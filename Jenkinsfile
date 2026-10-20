pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'ridhindas/mediplus'
        DOCKER_TAG = "${BUILD_NUMBER}"
        GIT_EMAIL = 'jenkins@example.com'
        GIT_NAME = 'Jenkins CI'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('SCA: Software Composition Analysis') {
            steps {
                sh '''
                    echo "=== Running SCA (Safety) ==="
                    source venv/bin/activate
                    safety check -r requirements.txt --json > sca-report.json || true
                    echo "SCA completed. Pipeline will not fail on vulnerabilities."
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'sca-report.json', allowEmptyArchive: true
                }
            }
        }
        
        stage('SAST: Static Application Security Testing') {
            steps {
                sh '''
                    echo "=== Running SAST (Bandit) ==="
                    source venv/bin/activate
                    bandit -r . -f json -o sast-report.json || true
                    echo "SAST completed. Pipeline will not fail on vulnerabilities."
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'sast-report.json', allowEmptyArchive: true
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "=== Building Docker Image ==="
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                '''
            }
        }
        
        stage('DAST: Dynamic Application Security Testing') {
            steps {
                sh '''
                    echo "=== Starting Dockerized App for DAST ==="
                    docker run -d --name mediplus-dast -p 8000:8000 ${DOCKER_IMAGE}:${DOCKER_TAG}
                    echo "Waiting 15 seconds for Django to start..."
                    sleep 15
                    
                    echo "=== Running DAST (OWASP ZAP) ==="
                    # --network host allows ZAP container to reach localhost:8000 on the EC2 host
                    docker run --rm --network host -v $(pwd):/zap/wrk/:rw \
                        owasp/zap2docker-stable zap-baseline.py \
                        -t http://localhost:8000 \
                        -J dast-report.json -r dast-report.html || true
                    
                    echo "=== Stopping and Removing Dockerized App ==="
                    docker stop mediplus-dast || true
                    docker rm mediplus-dast || true
                    echo "DAST completed and application removed."
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'dast-report.json, dast-report.html', allowEmptyArchive: true
                    // Ensure container is cleaned up even if pipeline is aborted
                    sh 'docker stop mediplus-dast || true; docker rm mediplus-dast || true'
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }
        
        stage('Update Kubernetes Manifests in Git') {
            steps {
                withCredentials([string(credentialsId: 'github-cred', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                        echo "=== Updating k8s/deployment.yaml with new image tag ==="
                        sed -i "s|image: .*|image: ${DOCKER_IMAGE}:${DOCKER_TAG}|g" k8s/deployment.yaml
                        
                        git config user.email "${GIT_EMAIL}"
                        git config user.name "${GIT_NAME}"
                        
                        # Use token for authentication
                        git remote set-url origin https://${GITHUB_TOKEN}@github.com/ridhindas/mediplus.git
                        
                        git add k8s/deployment.yaml
                        git commit -m "chore: update mediplus image to ${DOCKER_TAG} [skip ci]" || echo "No changes to commit"
                        git push origin HEAD:main || echo "Push failed or no changes"
                    '''
                }
            }
        }
    }
    
    post {
        always {
            echo "=== Pipeline Finished ==="
            echo "Security reports are available in the Jenkins Build Artifacts."
            echo "ArgoCD on your local machine will now detect the Git change and deploy."
            cleanWs()
        }
    }
}
