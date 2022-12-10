.EXPORT_ALL_VARIABLES:

POETRY ?= $(HOME)/.local/bin/poetry
DOTENV_BASE_FILE ?= .env
APP = telegram_bot_dosimeter

-include $(DOTENV_BASE_FILE)

.PHONY: install-poetry
install-poetry:  ## Installation Poetry tool for dependency management and packaging in Python
	curl -sSL https://install.python-poetry.org | python3 -

.PHONY: update-poetry
update-poetry:  ## Updating Poetry to the latest stable version
	$(POETRY) self update

.PHONY: run
run:  ## Run main function in main.py file - entry point in app
	$(POETRY) main-run

.PHONY: lint
lint:  ## Lint and static-check
	$(POETRY) run isort --check-only --diff $(APP)
	$(POETRY) run flake8 $(APP)
	$(POETRY) run black --check --diff $(APP)
	$(POETRY) run mypy $(APP) --show-error-codes

.PHONY: fmt-isort
fmt-isort:  ## To apply isort recursively
	$(POETRY) run isort $(APP)

.PHONY: fmt-black
fmt-black:  ## To get started black recursively
	$(POETRY) run black $(APP)

.PHONY: fmt
fmt: fmt-isort fmt-black

.PHONY: test
test:  ## Run tests
	$(POETRY) run pytest --numprocesses auto

.PHONY: test-coverage
test-coverage: ## Run tests with coverage
	$(POETRY) run pytest --cov=$(APP) --cov-report=html

.PHONY: clean
clean:  ## Clean up the __pycache__ folder
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
