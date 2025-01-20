# GitLab CI/CD Reusable Pipeline Module

This repository contains a reusable GitLab CI/CD pipeline setup that is modularized for easy use across multiple projects. The pipeline includes stages for building, tagging, and pushing Docker images to a registry. The configuration is split into individual files for each stage, making it easy to maintain and extend.

## Pipeline Structure

The GitLab CI/CD pipeline consists of the following stages:

- **Build:** Builds the Docker image.
- **Tag:** Increments the version and generates a tag for the Docker image.
- **Push:** Pushes the generated Docker image to a registry.

### Reusable Modules

Each stage is defined in a separate file, which can be reused across different projects:

- `.gitlab-ci.build.yml`: Defines the **build** stage.
- `.gitlab-ci.tag.yml`: Defines the **tag** stage.
- `.gitlab-ci.push.yml`: Defines the **push** stage.

### Main Pipeline File

The main `.gitlab-ci.yml` file includes these modules and sets up pipeline variables. It looks like this:

```yaml
# .gitlab-ci.yml
include:
  - local:.gitlab-ci.build.yml
  - local:.gitlab-ci.tag.yml
  - local:.gitlab-ci.push.yml

variables:
  IMAGE_NAME: registry.pgr.com/my-application # Replace with your registry/image name
  VERSION_FILE: VERSION # Version file location
  NODE_VERSION: v18.0 # Node.js version for tagging
  GITLAB_REPO: "http://gitlab-ci-token:${CI_JOB_TOKEN}@192.168.1.120/root/cicd-test.git" # Replace with your GitLab repository URL
  GIT_USER_NAME: "pgr-automation"
  GIT_USER_EMAIL: "grprashanth94@gmail.com"
```



# Templates
Create the Module Files
File: ```.gitlab-ci.build.yml```
```yaml
# Build stage
build:
  stage: build
  script:
    - echo "Building Docker image..."
  only:
    - branches
  tags:
    - k8s-runner
```
File: ```.gitlab-ci.tag.yml```
```yaml
# Tag stage
tag:
  stage: tag
  script:
    - echo "Generating new version..."
    # Ensure VERSION file exists
    - if [ ! -f $VERSION_FILE ]; then echo "0.0.0" > $VERSION_FILE; fi
    # Safely parse the version
    - cat $VERSION_FILE
    - OLD_VERSION=$(cat $VERSION_FILE)
    - MAJOR=$(echo $OLD_VERSION | cut -d. -f1)
    - MINOR=$(echo $OLD_VERSION | cut -d. -f2)
    - PATCH=$(echo $OLD_VERSION | cut -d. -f3)
    - PATCH=$((PATCH + 1)) # Increment the patch version
    - NEW_VERSION="$MAJOR.$MINOR.$PATCH"
    - echo $NEW_VERSION > $VERSION_FILE
    - echo $NEW_VERSION  
    # Prepare Docker tag
    - BRANCH_NAME=${CI_COMMIT_REF_NAME//\//-}
    - IMAGE_TAG="$BRANCH_NAME-node:$NEW_VERSION"
    - echo $IMAGE_TAG
    # Save tag for next stage
    - echo $IMAGE_TAG > image_tag.txt
    - echo "Commit updated version file"
    # Install Git if not available
    - apk update && apk add git
    # Check if the branch exists locally
    - git fetch
    - git branch -a
    - if ! git show-ref --verify --quiet refs/heads/$CI_COMMIT_REF_NAME; then git checkout -b $CI_COMMIT_REF_NAME; fi
    # Configure Git and commit changes
    - git config user.name "$GIT_USER_NAME"
    - git config user.email "$GIT_USER_EMAIL"
    - git add $VERSION_FILE
    - git commit -m "Increment version to $IMAGE_TAG [ci skip]"
    - git push $GITLAB_REPO $CI_COMMIT_REF_NAME
  artifacts:
    paths:
      - image_tag.txt
  tags:
    - k8s-runner
```
File: ```.gitlab-ci.push.yml```
```yaml
# Push stage
push:
  stage: push
  script:
    - echo "Pushing Docker image to registry..."
    - IMAGE_TAG=$(cat image_tag.txt)
    # Uncomment and configure docker login if needed
    # - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
    # - docker push $IMAGE_NAME:$IMAGE_TAG
  only:
    - branches
  tags:
    - k8s-runner
```
