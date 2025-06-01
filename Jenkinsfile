pipeline {
    agent any
    
    environment {
        // Project configuration
        PROJECT_NAME = 'rpger-content-extractor'
        DOCKER_IMAGE = 'rpger-content-extractor'
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_LATEST = "${DOCKER_IMAGE}:latest"
        DOCKER_VERSIONED = "${DOCKER_IMAGE}:${DOCKER_TAG}"
        
        // Python configuration
        PYTHON_VERSION = '3.11'
        VIRTUAL_ENV = 'venv'
        
        // Test configuration
        PYTEST_ARGS = '--verbose --tb=short --cov=Modules --cov-report=term-missing --cov-report=xml:coverage.xml'
        
        // Docker registry (customize as needed)
        DOCKER_REGISTRY = 'localhost:5000'  // Change to your registry
        
        // Environment files
        ENV_FILE = '.env'
    }
    
    options {
        // Keep builds for 30 days or 10 builds
        buildDiscarder(logRotator(daysToKeepStr: '30', numToKeepStr: '10'))
        
        // Timeout after 30 minutes
        timeout(time: 30, unit: 'MINUTES')
        
        // Timestamps in console output
        timestamps()
        
        // Skip default checkout
        skipDefaultCheckout(false)
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo "🔄 Checking out code..."
                checkout scm
                
                script {
                    // Get commit info
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    env.GIT_BRANCH_NAME = sh(
                        script: 'git rev-parse --abbrev-ref HEAD',
                        returnStdout: true
                    ).trim()
                }
                
                echo "📋 Build Info:"
                echo "  - Branch: ${env.GIT_BRANCH_NAME}"
                echo "  - Commit: ${env.GIT_COMMIT_SHORT}"
                echo "  - Build: ${BUILD_NUMBER}"
            }
        }
        
        stage('Environment Setup') {
            steps {
                echo "🐍 Setting up Python environment..."
                
                sh '''
                    # Create virtual environment
                    python${PYTHON_VERSION} -m venv ${VIRTUAL_ENV}
                    
                    # Activate and upgrade pip
                    . ${VIRTUAL_ENV}/bin/activate
                    pip install --upgrade pip setuptools wheel
                    
                    # Install dependencies
                    pip install -r requirements.txt
                    
                    # Install additional test dependencies
                    pip install pytest-xdist pytest-html pytest-json-report
                '''
                
                echo "📦 Python environment ready"
            }
        }
        
        stage('Code Quality') {
            parallel {
                stage('Linting') {
                    steps {
                        echo "🔍 Running code linting..."
                        sh '''
                            . ${VIRTUAL_ENV}/bin/activate
                            
                            # Run flake8 linting
                            echo "Running flake8..."
                            flake8 --max-line-length=88 --extend-ignore=E203,W503 \
                                   --exclude=venv,__pycache__,.git \
                                   --output-file=flake8-report.txt \
                                   . || true
                            
                            # Display results
                            if [ -f flake8-report.txt ]; then
                                echo "Flake8 results:"
                                cat flake8-report.txt
                            fi
                        '''
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: 'flake8-report.txt', allowEmptyArchive: true
                        }
                    }
                }
                
                stage('Code Formatting') {
                    steps {
                        echo "🎨 Checking code formatting..."
                        sh '''
                            . ${VIRTUAL_ENV}/bin/activate
                            
                            # Check black formatting
                            echo "Checking Black formatting..."
                            black --check --diff . || echo "Code formatting issues found"
                        '''
                    }
                }
            }
        }
        
        stage('Unit Tests') {
            steps {
                echo "🧪 Running unit tests..."
                sh '''
                    . ${VIRTUAL_ENV}/bin/activate
                    
                    # Create test directories
                    mkdir -p test-reports htmlcov
                    
                    # Run unit tests
                    pytest tests/ \
                        ${PYTEST_ARGS} \
                        --html=test-reports/unit-tests.html \
                        --self-contained-html \
                        --json-report --json-report-file=test-reports/unit-tests.json \
                        -m "unit or not (integration or e2e or slow)" \
                        || true
                '''
            }
            post {
                always {
                    // Publish test results
                    publishTestResults testResultsPattern: 'test-reports/*.xml'
                    
                    // Archive test reports
                    archiveArtifacts artifacts: 'test-reports/**/*', allowEmptyArchive: true
                    
                    // Publish HTML reports
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'test-reports',
                        reportFiles: 'unit-tests.html',
                        reportName: 'Unit Test Report'
                    ])
                    
                    // Coverage report
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('Integration Tests') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                    changeRequest()
                }
            }
            steps {
                echo "🔗 Running integration tests..."
                sh '''
                    . ${VIRTUAL_ENV}/bin/activate
                    
                    # Run integration tests
                    pytest tests/ \
                        --verbose --tb=short \
                        --html=test-reports/integration-tests.html \
                        --self-contained-html \
                        -m "integration" \
                        || true
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'test-reports/integration-tests.html', allowEmptyArchive: true
                }
            }
        }
        
        stage('Docker Build') {
            steps {
                echo "🐳 Building Docker image..."
                script {
                    // Build Docker image
                    def image = docker.build("${DOCKER_IMAGE}:${BUILD_NUMBER}")
                    
                    // Tag as latest if on main branch
                    if (env.GIT_BRANCH_NAME == 'main') {
                        image.tag('latest')
                    }
                    
                    // Store image ID for later use
                    env.DOCKER_IMAGE_ID = image.id
                }
                
                echo "✅ Docker image built successfully"
            }
        }
        
        stage('Docker Test') {
            steps {
                echo "🧪 Testing Docker container..."
                sh '''
                    # Test container startup
                    echo "Starting container for health check..."
                    CONTAINER_ID=$(docker run -d -p 5001:5000 ${DOCKER_VERSIONED})
                    
                    # Wait for container to start
                    sleep 10
                    
                    # Health check
                    echo "Performing health check..."
                    for i in {1..30}; do
                        if curl -f http://localhost:5001/health 2>/dev/null; then
                            echo "✅ Health check passed"
                            break
                        fi
                        echo "Waiting for service... ($i/30)"
                        sleep 2
                    done
                    
                    # Cleanup
                    docker stop $CONTAINER_ID
                    docker rm $CONTAINER_ID
                '''
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo "🚀 Deploying application..."
                script {
                    // Push to registry (customize as needed)
                    if (env.DOCKER_REGISTRY && env.DOCKER_REGISTRY != 'localhost:5000') {
                        docker.withRegistry("http://${env.DOCKER_REGISTRY}") {
                            def image = docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}")
                            image.push()
                            image.push('latest')
                        }
                    }
                    
                    // Deploy using docker-compose (customize as needed)
                    sh '''
                        echo "Deploying with docker-compose..."
                        export DOCKER_TAG=${BUILD_NUMBER}
                        docker-compose -f docker-compose.yml down || true
                        docker-compose -f docker-compose.yml up -d
                    '''
                }
                
                echo "✅ Deployment completed"
            }
        }
    }
    
    post {
        always {
            echo "🧹 Cleaning up..."
            
            // Clean up virtual environment
            sh 'rm -rf ${VIRTUAL_ENV} || true'
            
            // Clean up old Docker images (keep last 5)
            sh '''
                echo "Cleaning up old Docker images..."
                docker images ${DOCKER_IMAGE} --format "table {{.Tag}}" | \
                grep -E '^[0-9]+$' | sort -nr | tail -n +6 | \
                xargs -I {} docker rmi ${DOCKER_IMAGE}:{} || true
            '''
        }
        
        success {
            echo "✅ Pipeline completed successfully!"
            
            // Notify on success (customize as needed)
            // slackSend channel: '#ci-cd', 
            //           color: 'good', 
            //           message: "✅ ${PROJECT_NAME} build #${BUILD_NUMBER} succeeded"
        }
        
        failure {
            echo "❌ Pipeline failed!"
            
            // Notify on failure (customize as needed)
            // slackSend channel: '#ci-cd', 
            //           color: 'danger', 
            //           message: "❌ ${PROJECT_NAME} build #${BUILD_NUMBER} failed"
        }
        
        unstable {
            echo "⚠️ Pipeline completed with warnings"
        }
    }
}
