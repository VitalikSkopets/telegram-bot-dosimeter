.EXPORT_ALL_VARIABLES:

# Define color codes
RED       = \033[0;31m
YELLOW    = \033[0;33m
GREEN     = \033[0;32m
UNDERLINE = \033[4m
NC        = \033[0m

PYTHON := $(shell which python3)
POETRY := $(shell which poetry)

APP   = dosimeter
TESTS = tests/**/*.py

DOTENV_BASE_FILE ?= $(APP)/config/.env
POETRY_VERSION   ?= 1.8.4

-include $(DOTENV_BASE_FILE)

# ====================================
#               Poetry
# ====================================

.PHONY: install-poetry
install-poetry:  ## Installation Poetry tool for dependency management and packaging in Python
	curl -sSL https://install.python-poetry.org | python3 - --version $(POETRY_VERSION)
	export PATH="$HOME/.local/bin"
	@$(POETRY) --version

.PHONY: update-poetry
update-poetry:  ## Updating Poetry to the latest stable version
	@$(POETRY) self update

.PHONY: where-is-my-venv
where-is-my-venv:  ## Showing the directory where the interpreter is installed
	@$(POETRY) env info -p

# ====================================
#             Launch App
# ====================================

.PHONY: run
run:  ## Run main function in main.py file - entry point in app
	@$(POETRY) run main-run

# ====================================
#         Linters and formating
# ====================================

.PHONY: lint
lint:  ## Lint and static-check
	@echo "====> Checking started..."
	$(POETRY) run isort --check-only --diff $(APP)
	$(POETRY) run black --check --diff $(APP)
	$(POETRY) run ruff $(APP)
	$(POETRY) run mypy $(APP) $(TESTS) --show-error-codes
	$(POETRY) run yamllint -d '{"extends": "default", "ignore": ".venv"}' -s .
	@echo "$(GREEN)Linter and style checking finished! \(^_^)/$(NC)"

.PHONY: fmt-yaml
fmt-yaml:  ## to lint yaml files
	@$(POETRY) run yamllint -d '{"extends": "default", "ignore": ".venv"}' -s .

.PHONY: fmt-isort
fmt-isort:  ## To apply isort recursively
	@$(POETRY) run isort $(APP)

.PHONY: fmt-black
fmt-black:  ## To get started black recursively
	@$(POETRY) run black $(APP)

.PHONY: fmt
fmt: fmt-yaml fmt-isort fmt-black

.PHONY: mypy
mypy:  ## to run typing checking
	@$(POETRY) run mypy $(APP) $(TESTS) --show-error-codes

# ====================================
#               Tests
# ====================================

.PHONY: tests-all
tests-all:  ## Run all tests
	@$(POETRY) run pytest

.PHONY: tests
tests: ## Start tests only with specify markers option
	@$(POETRY) run pytest --verbose --randomly-seed=default -m $(opt) --no-cov --disable-warnings

.PHONY: tests-coverage
tests-coverage: ## Run tests with coverage
	@$(POETRY) run pytest --verbose --randomly-seed=default --cov=$(APP) --cov-report=term --cov-report=html

.PHONY: find-tests-slow
find-tests-slow: ## Find slow two tests
	@$(POETRY) run pytest --verbose --randomly-seed=default --durations=3 --no-cov --disable-warnings

.PHONY: tests-slow
tests-slow: ## Start tests with 'slow' mark
	@$(POETRY) run pytest --verbose --randomly-seed=default -m "slow" --no-cov --disable-warnings

.PHONY: tests-not-slow
tests-not-slow: ## Start quick tests (without 'slow' mark)
	@$(POETRY) run pytest --verbose --randomly-seed=default -m "not slow" --no-cov --disable-warnings

# ====================================
#               Cache
# ====================================

.PHONY: clean
clean:  ## Clean up the cache folders
	@rm -rf __pycache__ .DS_Store .pytest_cache .mypy_cache .ruff_cache coverage .coverage coverage.xml htmlcov
	@echo "$(GREEN)Cache folders deleted! \(^_^)/$(NC)"

# ====================================
#               Docker
# ====================================

.PHONY: docker-up
docker-up:  ## Launch docker container with bot
	docker-compose up -d --build

.PHONY: docker-down
docker-down:  ## Stop docker container with bot
	docker-compose down -v  && docker-compose ps

.PHONY: docker-restart
docker-restart: docker-down docker-up

.PHONY: docker-logs
docker-logs:  ## Show logs from docker container with bot
	docker-compose logs --follow