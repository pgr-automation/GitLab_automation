# Multi-Project Pipelines in GitLab

Multi-project pipelines in GitLab allow you to coordinate CI/CD processes across multiple repositories or projects. This is particularly useful when you have interdependent projects or need to trigger downstream pipelines.

---

## **1. Triggering a Downstream Pipeline**
You can trigger a downstream pipeline in another project using the `trigger` keyword.

```yaml
stages:
  - build
  - deploy

trigger_downstream:
  stage: deploy
  trigger:
    project: group/another-project # Specify the target project
    branch: main                  # Specify the branch to trigger
```

This triggers the pipeline in the specified project and branch.

---

## **2. Passing Variables to Downstream Pipelines**
You can pass custom variables to a downstream pipeline:

```yaml
stages:
  - deploy

trigger_downstream:
  stage: deploy
  trigger:
    project: group/another-project
    branch: main
  variables:
    ENVIRONMENT: production
    VERSION: "1.0.0"
```

The downstream pipeline can access these variables as environment variables.

---

## **3. Using Dynamic Child Pipelines**
Child pipelines allow dynamic generation of configurations. Use the `include` keyword to trigger child pipelines:

### Parent Pipeline
```yaml
stages:
  - generate
  - test

generate_pipeline:
  stage: generate
  script:
    - echo "Generating child pipeline..."
  trigger:
    include:
      - local: .child-pipeline.yml
```

### Child Pipeline (e.g., `.child-pipeline.yml`)
```yaml
stages:
  - test

test_job:
  stage: test
  script:
    - echo "Running tests in child pipeline"
```

This approach is helpful for splitting complex pipelines into smaller, manageable pieces.

---

## **4. Cross-Project Dependency Management**
If your projects depend on each other, you can use artifacts to share outputs between them.

### Upstream Project
```yaml
stages:
  - build

build_job:
  stage: build
  script:
    - make build
  artifacts:
    paths:
      - build-output/
```

### Downstream Project
```yaml
stages:
  - deploy

deploy_job:
  stage: deploy
  dependencies:
    - build_job
  script:
    - cp build-output/* ./
    - make deploy
```

The downstream project can access artifacts from the upstream project.

---

## **5. Visualizing Multi-Project Pipelines**
GitLab provides a **Pipeline Graph** to visualize how pipelines across multiple projects are connected. You can access this graph in the pipeline view to monitor execution and trace failures.

---

## **6. Combining Techniques**
Here’s an example combining triggers, variables, and artifacts:

### Upstream Project
```yaml
stages:
  - build

build_job:
  stage: build
  script:
    - make build
  artifacts:
    paths:
      - build-output/
  trigger:
    project: group/downstream-project
    branch: main
    variables:
      BUILD_STATUS: success
```

### Downstream Project
```yaml
stages:
  - deploy

deploy_job:
  stage: deploy
  script:
    - echo "Deploying with $BUILD_STATUS"
    - make deploy
  dependencies:
    - build_job
```

This integrates outputs and variables between pipelines.

---

Multi-project pipelines provide flexibility and scalability for complex workflows, enabling seamless coordination between repositories. Let me know if you need help setting up a specific configuration!

