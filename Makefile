mageBuild:

	docker build --build-arg PROJECT_NAME=stocks_crypto -t mageai/mageai .

mageRun:

	-docker rm -f unruffled_wilbur
	docker run -d --name unruffled_wilbur mageai/mageai

mageStart:

	docker start unruffled_wilbur

mageStop:

	docker stop unruffled_wilbur

supersetUp:

	docker-compose -f /Users/georgioszefkilis/superset/docker-compose-non-dev.yml up -d

supersetDown:

	docker-compose -f /Users/georgioszefkilis/superset/docker-compose-non-dev.yml down
