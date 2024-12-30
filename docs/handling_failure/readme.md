# Handling Job Failures in GitLab CI/CD

Effectively managing job failures in GitLab CI/CD pipelines ensures robustness and reliability. Below are strategies for handling failures in various scenarios:

---

## **1. Retry Failed Jobs Automatically**
Use the `retry` keyword to retry a job multiple times before marking it as failed:

```yaml
stages:
  - build

build_job:
  stage: build
  script:
    - make build
  retry:
    max: 3          # Retry up to 3 times
    when: always     # Retry on any failure (other options: `script_failure`, `runner_system_failure`, etc.)
```

---

## **2. Allow Job Failures Without Breaking the Pipeline**
Use the `allow_failure` keyword to allow a job to fail without affecting the pipeline status:

```yaml
stages:
  - test

test_job:
  stage: test
  script:
    - ./run_tests
  allow_failure: true
```

This is useful for optional checks or experimental jobs.

---

## **3. Use `when: on_failure` to Run Recovery or Debug Jobs**
Define jobs that execute only when a previous job fails:

```yaml
stages:
  - test
  - recover

test_job:
  stage: test
  script:
    - ./run_tests

recover_job:
  stage: recover
  script:
    - echo "Recovering from failure..."
  when: on_failure
```

---

## **4. Conditional Execution Based on Status**
Use `rules` to run jobs conditionally based on pipeline or job status:

```yaml
stages:
  - deploy

deploy_job:
  stage: deploy
  script:
    - echo "Deploying to production"
  rules:
    - if: $CI_PIPELINE_STATUS == "success"
```

---

## **5. Add Timeout to Prevent Stuck Jobs**
Set a timeout to fail jobs that take too long:

```yaml
stages:
  - build

build_job:
  stage: build
  script:
    - make build
  timeout: 10m  # Timeout after 10 minutes
```

---

## **6. Use `dependencies` to Skip Jobs if a Dependency Fails**
Control job execution based on the success of dependent jobs:

```yaml
stages:
  - build
  - test

build_job:
  stage: build
  script:
    - make build

test_job:
  stage: test
  script:
    - ./run_tests
  dependencies:
    - build_job
```

---

## **7. Notifications on Failure**
Send notifications when jobs fail:

```yaml
failure_notification:
  stage: notify
  script:
    - echo "Sending failure notification"
  when: on_failure
```

Integrate with tools like Slack or email to alert your team.

---

## **8. Using `needs` for Better Failure Management**
Define job dependencies explicitly to control execution flow:

```yaml
stages:
  - build
  - test

build_job:
  stage: build
  script:
    - make build

test_job:
  stage: test
  script:
    - ./run_tests
  needs:
    - build_job
```

This ensures dependent jobs don’t block others unnecessarily.

---

## **Combining Techniques**
Here’s an example combining retries, allowing failures, and recovery jobs:

```yaml
stages:
  - build
  - test
  - recover

build_job:
  stage: build
  script:
    - make build
  retry:
    max: 3

test_job:
  stage: test
  script:
    - ./run_tests
  allow_failure: true

recover_job:
  stage: recover
  script:
    - echo "Recovering..."
  when: on_failure
```

---

Using these techniques ensures that your pipeline handles failures gracefully while maintaining flexibility and reliability.

