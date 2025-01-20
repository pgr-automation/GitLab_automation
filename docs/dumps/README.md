1. Git tags for docker image versions
```bash
git add .;git commit -m "v0.0.2" && git tag -a v0.0.2 -m "Tag message for version v0.0.2" && git push origin main  --tags
```
```yaml
image: maven:3.8.1-jdk-11

stages:
  - build
  - test
  - package
  - docker_build
  - deploy
  - rollback
  ##

variables:
  DOCKER_IMAGE: 9902736822/my-java-app
  DOCKER_HOST: tcp://docker:2375
  DOCKER_DRIVER: overlay2

before_script:
  - cd my_java_app

cache:
  paths:
    - .m2/repository

workflow:
  rules:
    - if: '$CI_COMMIT_REF_NAME == "main"'

build:
  stage: build
  script:
    - mvn clean compile
  tags:
    - k8s-runner

test:
  stage: test
  script:
    - mvn test
  tags:
    - k8s-runner
package:
  stage: package
  script:
    - mvn package
  artifacts:
    paths:
      - ./my_java_app/target/*.jar
  tags: 
    - k8s-runner

docker-build:
  stage: docker_build
  image: docker:latest
  services:
    - name: docker:19.03.12-dind
      command: ["--host=tcp://docker:2375"]
  before_script:
    - unset DOCKER_HOST
  script:
    - |
      echo "Fetch and determine the latest version tag"
      git fetch --tags
      LATEST_TAG=$(git describe --tags $(git rev-list --tags --max-count=1) || echo "latest")
      echo "Latest tag: $LATEST_TAG"

      echo "Build and push Docker image"
      docker login -u $dkr_username -p $dkr_password
      ls -lrth  my_java_app 
      cd my_java_app
      whoami
      ps -ef
      whoami
      docker build -t $DOCKER_IMAGE:$LATEST_TAG .
      docker push $DOCKER_IMAGE:$LATEST_TAG

      echo "Save the new tag for later use"
      echo $LATEST_TAG > .version_tag

  artifacts:
    paths:
      - .version_tag
  tags:
    - k8s-runner

#
docker_deploy:
  stage: deploy
  image: docker:latest
  services:
    - name: docker:24.0.5-dind
      command: ["--host=tcp://0.0.0.0:2375"]  # Expose Docker API for communication
  script: 
    - |
      # Fetch the latest tag or default to "latest"
      TAG=$(git describe --tags $(git rev-list --tags --max-count=1) || echo "latest")
      echo "Deploying with tag: $TAG"

      # Check if a container named "myapp" is already running and remove it
      if [ $(docker ps -a -q -f name=myapp) ]; then
        docker stop myapp
        docker rm myapp
      fi

      # Run the new container with the correct tag
      docker run --name myapp -d "$DOCKER_IMAGE:$TAG"
      
      # Verify if the container is running
      echo "Verifying if the container is running..."
      sleep 5
      if [ ! $(docker ps -q -f name=myapp) ]; then
        echo "Deployment failed: Container is not running."
        exit 1
      fi

      # Optionally, check the logs to verify the application started correctly
      docker logs myapp | tail -n 10

      echo "Deployment successful. Removing the previous container."
      REMOVE_TAG=$(git tag -l | sort -V | tail -n 3 | head -n 1)
      docker rmi "$DOCKER_IMAGE:$REMOVE_TAG"


  
rollback:
  stage: rollback
  image: docker:latest
  services:
    - docker:24.0.5-dind
  script:
    - |
      echo "Rolling back to the previous stable version"

      # Fetch the last successful tag (replace this with your own logic if needed)
      PREVIOUS_TAG=$(git tag -l | sort -V | tail -n 2 | head -n 1)
      echo "Rolling back to tag: $PREVIOUS_TAG"

      # Remove the failed container if it exists
      if [ $(docker ps -a -q -f name=myapp) ]; then
        docker stop myapp
        docker rm myapp
      fi

      # Run the previous stable container
      docker run --name myapp -d "$DOCKER_IMAGE:$PREVIOUS_TAG"
  when: on_failure
  allow_failure: false
#
```


# incremental tag

```yaml
stages:
  - build
  - tag
  - push

variables:
  IMAGE_NAME: registry.pgr.com/my-application # Replace with your registry/image name
  VERSION_FILE: VERSION

build:
  stage: build
  script:
    - echo "Building Docker image..."
    - docker build -t $IMAGE_NAME:latest .
  only:
    - branches

tag:
  stage: tag
  script:
    - echo "Generating new version..."
    # Increment the version
    - OLD_VERSION=$(cat $VERSION_FILE)
    - IFS='.' read -r MAJOR MINOR PATCH <<< "$OLD_VERSION"
    - PATCH=$((PATCH + 1))
    - NEW_VERSION="$MAJOR.$MINOR.$PATCH"
    - echo $NEW_VERSION > $VERSION_FILE
    - echo "New version: $NEW_VERSION"
    # Commit the updated version file
    - git config user.name "GitLab CI"
    - git config user.email "ci@example.com"
    - git add $VERSION_FILE
    - git commit -m "CI: Increment version to $NEW_VERSION"
    - git push origin $CI_COMMIT_REF_NAME
    # Tag the Docker image
    - docker tag $IMAGE_NAME:latest $IMAGE_NAME:$NEW_VERSION

push:
  stage: push
  script:
    - echo "Pushing Docker image to registry..."
    - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
    - docker push $IMAGE_NAME:latest
    - docker push $IMAGE_NAME:$NEW_VERSION
  only:
    - branches
```
# Steps to Resolve the 403 Error:

```text
Steps to Resolve the 403 Error:

    Check GitLab CI Token Permissions:
        The GitLab CI runner uses a token (in your case, gitlab-ci-token:[MASKED]) to authenticate. This token may not have sufficient permissions to push code to the repository.
        Ensure that the user associated with the GitLab CI token has permission to push to the repository.

    Ensure Correct Access Rights:
        Check the access rights of the GitLab CI token. Go to your GitLab project, then navigate to Settings > CI / CD > Secret Variables, and confirm that the user or token you're using has the correct permissions to push code.

    Update CI/CD Configuration:
        Sometimes, you may need to explicit

Solution Using Personal Access Token (PAT):

    Generate a Personal Access Token (PAT):
        Go to your GitLab account.
        Navigate to Profile > Preferences > Access Tokens.
        Generate a token with write_repository permission (this gives permission to push changes to the repository).

    Set the Token in GitLab CI/CD Environment Variables:
        Go to Project Settings > CI / CD > Variables.
        Add a new variable CI_JOB_TOKEN with the value being the personal access token you generated.

    Modify .gitlab-ci.yml to Use the Token:
        Use the token in the git push command as follows:

```
