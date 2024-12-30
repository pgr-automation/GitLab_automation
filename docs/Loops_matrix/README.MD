# Using the parallel: matrix Strategy (For Job Loops)

The matrix strategy allows you to define multiple configurations for a single job and execute them in parallel.
```yaml
stages:
  - test

test_job:
  stage: test
  script:
    - echo "Testing $ENVIRONMENT"
  parallel:
    matrix:
      - ENVIRONMENT: ["dev", "staging", "production"]
```