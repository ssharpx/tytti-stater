.PHONY: help up down restart rebuild logs logs-db ps shell db-shell db-backup db-restore clean

COMPOSE = docker compose
BOT = bot
DB = database

include .env
export

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

up: ## Build and start all services in background
	$(COMPOSE) up -d --build

down: ## Stop and remove containers
	$(COMPOSE) down

restart: ## Restart the bot
	$(COMPOSE) restart $(BOT)

rebuild: ## Rebuild the bot without cache and restart
	$(COMPOSE) build --no-cache $(BOT)
	$(COMPOSE) up -d $(BOT)

logs: ## Follow bot logs
	$(COMPOSE) logs -f --tail=100 $(BOT)

logs-db: ## Follow database logs
	$(COMPOSE) logs -f --tail=100 $(DB)

ps: ## Show container status
	$(COMPOSE) ps

shell: ## Open a shell in the bot container
	$(COMPOSE) exec $(BOT) bash

db-shell: ## Open psql
	$(COMPOSE) exec $(DB) psql -U $(DB_USER) -d $(DB_NAME)

db-backup: ## Dump the database to backups/
	@mkdir -p backups
	$(COMPOSE) exec -T $(DB) pg_dump -U $(DB_USER) $(DB_NAME) > backups/$(DB_NAME)_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Backup saved to backups/"

db-restore: ## Restore the database: make db-restore FILE=backups/xxx.sql
	@test -n "$(FILE)" || (echo "Error: specify FILE=path/to/dump.sql" && exit 1)
	$(COMPOSE) exec -T $(DB) psql -U $(DB_USER) -d $(DB_NAME) < $(FILE)

clean:  ## Stop containers and DELETE all database data
	@read -p "This will delete all database data. Continue? [y/N] " ans && [ "$$ans" = "y" ]
	$(COMPOSE) down -v