PROJECT_ID = summary-publication
REGION = southamerica-east1
JOB_NAME = email-job
IMAGE_NAME = gcr.io/$(PROJECT_ID)/$(JOB_NAME)

.PHONY: config build deploy

config:
	gcloud config set project $(PROJECT_ID)

build:
	gcloud builds submit --tag $(IMAGE_NAME)

deploy: build
	gcloud beta run jobs update $(JOB_NAME) \
		--image $(IMAGE_NAME) \
		--region $(REGION)
