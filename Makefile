.EXPORT_ALL_VARIABLES:
POETRY ?= $(HOME)/.poetry/bin/poetry
DOTENV_BASE_FILE ?= .env
APP = telegram_bot_dosimeter

-include $(DOTENV_BASE_FILE)

install-poetry:  ## Installation Poetry tool for dependency management and packaging in Python
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

update-poetry:  ## Updating Poetry to the latest stable version
	$(POETRY) self update

run:  ## Run main function in main.py file - entry point in app
	$(POETRY) main-run

lint:  ## Lint and static-check
	$(POETRY) run isort --check-only --diff .
	$(POETRY) run flake8 $(APP)
	$(POETRY) run black --check --diff .
	$(POETRY) run mypy $(APP) --show-error-codes

fmt-isort:  ## To apply isort recursively
	$(POETRY) run isort .

fmt-black:  ## To get started black recursively
	$(POETRY) run black .

fmt: fmt-isort fmt-black

test:  ## Run tests
	$(POETRY) run pytest --numprocesses auto

test-coverage: ## Run tests with coverage
	$(POETRY) run pytest --cov=$(APP) --cov-report=html

clean:  ## Clean up the __pycache__ folder
	rm -rf __pycache__
	rm -rf .pytest_cache


.PHONY: install-poetry update-poetry run lint fmt-isort fmt-black fmt test test-coverage clean
