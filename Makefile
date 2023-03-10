DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_FILE = docker-compose.yaml

.PHONY: start stop restart status clean test test_local

start: ## Start all or c=<name> containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d $(c)

stop: ## Stop all or c=<name> containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) stop $(c)

status: ## Show status of containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) ps

restart: ## Restart all or c=<name> containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) stop $(c)
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up $(c) -d

logs: ## Show logs for all or c=<name> containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) logs --tail=100 -f $(c)

clean: ## Clean all data
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

test_local: ## Run tests
	export API_PORT=8000  &&\
	export DB_PORT=5432 &&\
	export POSTGRES_USER=ciplay &&\
	export POSTGRES_DATABASE=ciplay &&\
	export POSTGRES_PASSWORD=ciplay &&\
	export DB_SERVICE_NAME=localhost &&\
	python -m pytest tests/;

test: ## Run tests in Docker
	 docker-compose exec api python -m pytest tests/
