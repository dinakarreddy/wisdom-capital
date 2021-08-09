DEPENDENT_SERVICE_DOCKER_COMPOSE_FILE=$(shell pwd)/dependent_docker_services/docker-compose.yml
DOCKER_NETWORK=wisdom_network

start-dependencies: check-pre-requisites
	@command docker-compose -f $(DEPENDENT_SERVICE_DOCKER_COMPOSE_FILE) up -d
	@command ./dependent_docker_services/startup_scripts/wait_for_dependent_services_to_start.sh

stop-dependencies: check-pre-requisites
	@command docker-compose -f $(DEPENDENT_SERVICE_DOCKER_COMPOSE_FILE) down || (echo "Already stopped")

check-pre-requisites:
	@command -v docker || (echo "Docker not installed!" && exit 1)
	@command -v docker-compose || (echo "Docker compose not installed!" && exit 1)
