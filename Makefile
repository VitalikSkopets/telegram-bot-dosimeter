.EXPORT_ALL_VARIABLES:

APP = dosimeter
DOTENV_BASE_FILE ?= $(APP)/config/.env
TESTS = tests/**/*.py

-include $(DOTENV_BASE_FILE)

# ==== Poetry ====

.PHONY: install-poetry
install-poetry:  ## Installation Poetry tool for dependency management and packaging in Python
	curl -sSL https://install.python-poetry.org | python3 -
	export PATH="/root/.local/bin:$PATH"
	poetry --version

.PHONY: update-poetry
update-poetry:  ## Updating Poetry to the latest stable version
	poetry self update

# ==== Launch App ====

.PHONY: run
run:  ## Run main function in main.py file - entry point in app
	poetry run main-run

# ==== Linters and formating ====

.PHONY: lint
lint:  ## Lint and static-check
	@echo "====> Checking started..."
	poetry run isort --check-only --diff $(APP)
	poetry run black --check --diff $(APP)
	poetry run ruff $(APP)
	poetry run mypy $(APP) $(TESTS) --show-error-codes
	poetry run yamllint -d '{"extends": "default", "ignore": ".venv"}' -s .
	@echo "====> Linter and style checking finished! \(^_^)/"

.PHONY: fmt-yaml
fmt-yaml:  ## to lint yaml files
	poetry run yamllint -d '{"extends": "default", "ignore": ".venv"}' -s .

.PHONY: fmt-isort
fmt-isort:  ## To apply isort recursively
	poetry run isort $(APP)

.PHONY: fmt-black
fmt-black:  ## To get started black recursively
	poetry run black $(APP)

.PHONY: fmt
fmt: fmt-yaml fmt-isort fmt-black

.PHONY: mypy
mypy:  ## to run typing checking
	poetry run mypy $(APP) $(TESTS) --show-error-codes

# ==== Tests ====

.PHONY: test
test:  ## Run tests
	poetry run pytest --verbose --randomly-seed=default --capture=no --showlocals

.PHONY: test-coverage
test-coverage: ## Run tests with coverage
	poetry run pytest --verbose --randomly-seed=default --cov=$(APP) --cov-report=term --cov-report=html

.PHONY: find-tests-slow
find-tests-slow: ## Find slow two tests
	poetry run pytest --verbose --randomly-seed=default --durations=2 --no-cov --disable-warnings

.PHONY: tests-slow
tests-slow: ## Start tests with 'slow' mark
	poetry run pytest --verbose --randomly-seed=default -m "slow" --no-cov --disable-warnings

.PHONY: tests-not-slow
tests-not-slow: ## Start quick tests (without 'slow' mark)
	pytest --verbose --randomly-seed=default -m "not slow" --no-cov --disable-warnings

.PHONY: tests-encryption
tests-encryption: ## Start tests with 'login' mark
	pytest --verbose --randomly-seed=default -m "encryption" --no-cov --disable-warnings

.PHONY: tests-message-engine
tests-message-engine: ## Start tests with 'message_engine' mark
	pytest --verbose --randomly-seed=default -m "message_engine" --no-cov --disable-warnings

.PHONY: tests-parse
tests-parse: ## Start tests with 'parsing' mark
	pytest --verbose --randomly-seed=default -m "parsing" --no-cov --disable-warnings

.PHONY: tests-api
tests-api: ## Start tests with 'api' mark
	pytest --verbose --randomly-seed=default -m "api" --no-cov --disable-warnings

.PHONY: tests-navigator
tests-navigator: ## Start tests with 'navigator' mark
	pytest --verbose --randomly-seed=default -m "navigator" --no-cov --disable-warnings

.PHONY: tests-analytics
tests-analytics: ## Start tests with 'analytics' mark
	pytest --verbose --randomly-seed=default -m "analytics" --no-cov --disable-warnings

.PHONY: tests-bot
tests-bot: ## Start tests with 'bot' mark
	pytest --verbose --randomly-seed=default -m "bot" --no-cov --disable-warnings

# ==== Cache ====

.PHONY: clean
clean:  ## Clean up the cache folders
	@rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache .coverage coverage.xml htmlcov
	@echo "====> Cache folders deleted! \(^_^)/"
