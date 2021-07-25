.PHONY: build aws
IMAGE=ci_pd_jina
REGION=eu-west-2
ACCOUNT=700478082539
REPO=$(ACCOUNT).dkr.ecr.$(REGION).amazonaws.com

build_app:
	docker build --target app -t $(IMAGE) .

build_tests:
	docker build --target tests -t $(IMAGE)_tests .

local: build_app
	docker run --rm -p 8080:8080 $(IMAGE)

login:
	aws ecr get-login-password --region $(REGION) | \
		docker login --username AWS \
					 --password-stdin $(REPO)

aws: login build_app
	docker tag $(IMAGE) $(REPO)/$(IMAGE)
	docker push $(REPO)/$(IMAGE)

deploy: aws
	aws lambda update-function-code \
		--function-name $(IMAGE) \
		--image-uri $(REPO)/$(IMAGE):latest
	aws lambda wait function-updated \
		--function-name $(IMAGE)

docker_tests:
	docker-compose -f docker-compose-tests.yaml build
	docker-compose -f docker-compose-tests.yaml up --exit-code-from app
