.EXPORT_ALL_VARIABLES:
POETRY ?= $(HOME)/.poetry/bin/poetry
DOTENV_BASE_FILE ?= .env
APP = telegram_bot_dosimeter

-include $(DOTENV_BASE_FILE)

run:  ## Run main function in main.py file - entry point in app
	$(POETRY) main-run

lint:  ## Lint and static-check
	$(POETRY) run isort .
	$(POETRY) run flake8 $(APP)
	$(POETRY) run black .
	$(POETRY) run mypy $(APP)

test: lint  ## Run tests
	$(POETRY) run pytest --numprocesses auto

test-coverage: ## Run tests with coverage
	$(POETRY) run pytest --cov=$(APP) --cov-report=html

clean:  ## Clean up the __pycache__ folder
	rm -rf __pycache__
	rm -rf .pytest_cache


.PHONY: run lint test test-coverage clean
