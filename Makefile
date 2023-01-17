DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_FILE = docker-compose.yaml

.PHONY: start stop restart status clean test

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

database: ## Create database
	docker run --name ciplay_db -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres
	docker cp sql_scripts/create_db.sql ciplay_db:/docker-entrypoint-initdb.d/create_db.sql
	docker cp sql_scripts/procedures.sql ciplay_db:/docker-entrypoint-initdb.d/procedures.sql
	docker exec -u postgres ciplay_db psql postgres postgres -f docker-entrypoint-initdb.d/create_db.sql
	docker exec -u postgres ciplay_db psql postgres postgres -f docker-entrypoint-initdb.d/procedures.sql

test: ## Run tests
	echo 'TESTING...'