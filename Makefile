# Color Config
NOCOLOR=\033[0m
GREEN=\033[0;32m
BGREEN=\033[1;32m
YELLOW=\033[0;33m
CYAN=\033[0;36m
RED=\033[0;31m

# Config
BREAK=\n

# Default action
.DEFAULT_GOAL := help


# .PHONY targets
.PHONY: \
  help \
  build rebuild fix-permissions up restart stop destroy logs \
  export import export-collections import-collections docker-build docker-run compose-up compose-down


# Checks if the docker-compose command is available in the system
DOCKER_COMPOSE := $(shell command -v docker-compose 2> /dev/null)

ifeq ($(strip $(DOCKER_COMPOSE)),)
	DOCKER_COMPOSE := docker compose
else
	DOCKER_COMPOSE := docker-compose
endif

## General commands:
help: ## Display this message help
	@awk '\
		BEGIN {\
			FS = ":.*##";\
			printf "${BREAK}${YELLOW}Usage:${BREAK}${CYAN}  make [target]${BREAK}${BREAK}${YELLOW}Available targets:${BREAK}${BREAK}" \
		} /^##/ { \
			printf "${YELLOW}%s${NOCOLOR}${BREAK}", substr($$0, 4) \
		} /^[a-zA-Z0-9_-]+:.*?##/ { \
			printf "  ${BGREEN}%-18s${NOCOLOR} %s${BREAK}", $$1, $$2 \
		}' $(MAKEFILE_LIST)
		@printf "${BREAK}${YELLOW}Examples:${BREAK}${CYAN}  make up${BREAK}"
		@printf "${CYAN}  make COMMAND c='PARAM'${BREAK}"

build: ## Build all container
	@echo ""
	@echo "${YELLOW}Build all container${NOCOLOR}"
	@echo ""
	$(DOCKER_COMPOSE) up --build -d

rebuild: destroy build ## Rebuild all container

up: ## Start all container in detached mode
	@echo ""
	@echo "${YELLOW}Start all container${NOCOLOR}"
	@echo ""
	$(DOCKER_COMPOSE) up -d;

restart: stop up ## Restart all container

stop: ## Stop all container
	@echo ""
	@echo "${YELLOW}Stop all container${NOCOLOR}"
	@echo ""
	$(DOCKER_COMPOSE) stop

destroy: ## Destroy all container
	@echo ""
	@echo "${RED}Warning: This will destroy all container and data${NOCOLOR}"
	@echo "${YELLOW}Destroy all container${NOCOLOR}"
	@echo ""
	$(DOCKER_COMPOSE) down --remove-orphans -v

logs: ## See LOG in container syncdb
	@echo ""
	@echo "${YELLOW}Log in syncdb container${NOCOLOR}"
	@echo ""
	$(DOCKER_COMPOSE) logs -f syncdb

## MongoSync commands:
bash: ## Open bash in syncdb container
	$(DOCKER_COMPOSE) exec syncdb bash

## Export commands:
export: ## Export all collections
	@echo "${CYAN}Running full export...${NOCOLOR}"
	$(DOCKER_COMPOSE) run --rm syncdb python3 main.py export

export-filter: ## Export by filter: make export-filter f='{"connectionId": "..."}'
	@echo "${CYAN}Exporting documents with filter: $(f)${NOCOLOR}"
	$(DOCKER_COMPOSE) run --rm syncdb python3 main.py export --query '$(f)'

export-collections: ## Export specific collections: make export-collections c='collection1 collection2'
	@echo "${CYAN}Exporting collections: $(c)${NOCOLOR}"
	$(DOCKER_COMPOSE) run --rm syncdb python3 main.py export --collections $(c)

## Import commands:
import: ## Import all collections
	@echo "${CYAN}Running full import...${NOCOLOR}"
	$(DOCKER_COMPOSE) run --rm syncdb python3 main.py import

import-collections: ## Import specific collections: make import-collections c='collection1 collection2'
	@echo "${CYAN}Importing collections: $(c)${NOCOLOR}"
	$(DOCKER_COMPOSE) run --rm syncdb python3 main.py import --collections $(c)

## Update output commands:
patch: ## Patch using filter and update dicts: make patch f='{"id": "..."}' u='{"id": "..."}'
	@echo "${CYAN}Patching documents: filter=$(f) update=$(u)${NOCOLOR}"
	$(DOCKER_COMPOSE) run --rm syncdb python3 main.py patch --filter '$(f)' --update '$(u)'

# Ignore make target errors for commands like `make import `
.PHONY: %
%:
	@: