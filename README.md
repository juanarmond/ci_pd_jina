# cipd_backend_ds

# Tests
To run tests run: `./docker_run.sh pytest`

# Deployment
## Intially:
1) Create ECR
2) Create initial lambda function

## After:
1) Make sure the env vars are present in github settings look at deploy.yaml where they are used:
 - AWS_ACCESS_KEY_ID
 - AWS_SECRET_ACCESS_KEY
 - AWS_DEFAULT_REGION
2) make deploy

## AWS settings:
1) Make sure the lambda function has the env vars:
 - DYNACONF_WEAVIATE__server
 - DYNACONF_WEAVIATE__port
 - DYNACONF_MODEL__path