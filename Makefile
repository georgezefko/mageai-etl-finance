CONTAINER_NAME ?= unruffled_wilbur
IMAGE_TAG ?= mageai/mageai
mageBuild:

	docker build --build-arg PROJECT_NAME=stocks_crypto -t $(IMAGE_TAG) .

mageRun:

	-docker rm -f $(CONTAINER_NAME)
	docker run -d --name $(CONTAINER_NAME) $(IMAGE_TAG)

mageStart:

	docker start $(CONTAINER_NAME)

mageStop:

	docker stop $(CONTAINER_NAME)

supersetUp:

	docker-compose -f /Users/georgioszefkilis/superset/docker-compose-non-dev.yml up -d

supersetDown:

	docker-compose -f /Users/georgioszefkilis/superset/docker-compose-non-dev.yml down
