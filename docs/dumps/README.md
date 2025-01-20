1. Git tags for docker image versions
```bash
git add .;git commit -m "v0.0.2" && git tag -a v0.0.2 -m "Tag message for version v0.0.2" && git push origin main  --tags
```

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
