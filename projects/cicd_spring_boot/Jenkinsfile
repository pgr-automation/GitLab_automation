pipeline{
    environment {
        Docker_image = "9902736822/springbootapp:${Build_Version}"
        SONAR_URL = "http://192.168.1.130:9000" 
        DOCKER_REGISTRY = "https://hub.docker.com/"
        DOCKER_CREDENTIALS_ID = "1001"
        
    }
    agent {
        docker { image '9902736822/ubunu_java:v2.0.0'
        args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
    }
    }
    
    stages{
        stage('Git check out'){
            steps{
                script{
                    git branch: 'main', credentialsId: '28059df9-d0e4-49f6-9da6-e410f9470aff', url: 'https://github.com/pgr-automation/CICD_spring_boot.git'
                    
                }
            }
        }
        stage("build"){
            steps{
                sh '''
                hostname
                ip r l
                cd spring-bootapp/
                export MAVEN_OPTS="--add-opens java.base/java.lang=ALL-UNNAMED"
                mvn clean package 
            
                '''
            }
        }
        stage('SonarQube Code Analysis'){
            steps{
                withCredentials([string(credentialsId: 'SonarQube', variable: 'SONAR_AUTH_TOKEN')]) {
                    sh '''
                        hostname
                        ip r l
                        cd spring-bootapp/
                        mvn sonar:sonar -Dsonar.login=$SONAR_AUTH_TOKEN -Dsonar.host.url=${SONAR_URL}

                        '''
                }

            }
        }
        
        stage('Docker Image Build'){
             
            steps{
                sh '''
                    hostname
                    ip r l
                    cd spring-bootapp/  
                    docker build -t ${Docker_image} .
                '''
            }
        }
        stage('Image scan using trivy'){
            
            steps {
                script{
                    def scanResult = sh(script: "trivy image --exit-code 1 --severity HIGH,CRITICAL ${Docker_image}", returnStatus: true)
                    if (scanResult != 0){
                        error "Image scanning failed. High or Critical vulnerabilities found."
                    }
                    else {
                        echo "Image Passed Vulnerabilities Scan "
                    }
                }
               
            
            }
            
        }

        stage('Tag Image and Push to registry'){
            steps{
                script{
                    withCredentials([string(credentialsId: 'registry_passwd', variable: 'registry_pwd')]) {
                        sh '''
                        hostname
                        ip r l
                        docker login -u 9902736822 -p ${registry_pwd}
                        docker tag ${Docker_image} ${Docker_image}
                        docker push ${Docker_image}
                        '''

                    }
                }

            }
        }
        
        stage('Deleting Old Version Image'){
            
            steps{
                sh '''
                hostname
                ip r l
                docker rmi -f 9902736822/springbootapp:${Del_Version}
                docker rmi -f springbootapp:${Del_Version}
                docker rmi -f springbootapp:${Build_Version}
                '''
            }
        }
        stage('Updating k8s deployment manifest file') {
            environment {
                REPO_NAME = "CICD_spring_boot-_k8s_Deployment_manifest"
                USER_NAME = "pgr-automation"
                USER_EMAIL = "grprashanth94@gmail.com"  // Corrected the email address
            }
            steps {
                withCredentials([string(credentialsId: 'HTTPS_GITHUB', variable: 'Git_token')]) {
                    sh '''
                        mkdir -p /var/lib/jenkins/automation/${REPO_NAME}
                        cd /var/lib/jenkins/automation/${REPO_NAME}
                        if [ ! -d ".git" ]; then 
                            git clone https://${Git_token}:x-oauth-basic@github.com/pgr-automation/${REPO_NAME}.git .
                        fi                    
                        
                        git config user.email "${USER_EMAIL}"
                        git config user.name "${USER_NAME}"
                        cd spring_boot
                        cp -f /var/lib/jenkins/workspace/CICD_spring_boot_app/Deployment.yml .
                        sed -i "s|release-image|${Docker_image}|g" Deployment.yml
                        git add Deployment.yml
                        git commit -m "new release ${Docker_image}" 
                        git push https://${Git_token}:x-oauth-basic@github.com/pgr-automation/${REPO_NAME}.git HEAD:main
                        git log 
                    '''
                }
            }
        }
    }   
        
    
}