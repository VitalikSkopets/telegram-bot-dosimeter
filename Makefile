.EXPORT_ALL_VARIABLES:

DOTENV_BASE_FILE ?= .env
APP = dosimeter

-include $(DOTENV_BASE_FILE)

# === Poetry ===

.PHONY: install-poetry
install-poetry:  ## Installation Poetry tool for dependency management and packaging in Python
	curl -sSL https://install.python-poetry.org | python3 -
	export PATH="/root/.local/bin:$PATH"
	poetry --version

.PHONY: update-poetry
update-poetry:  ## Updating Poetry to the latest stable version
	poetry self update

# === Launch App ===

.PHONY: run
run:  ## Run main function in main.py file - entry point in app
	poetry run main-run

# === Linters and formating ===

.PHONY: lint
lint:  ## Lint and static-check
	@echo "====> Checking started..."
	poetry run isort --check-only --diff $(APP)
	poetry run black --check --diff $(APP)
	poetry run ruff $(APP)
	poetry run mypy $(APP) --show-error-codes
	@echo "====> Linter and style checking finished! \(^_^)/"

.PHONY: fmt-isort
fmt-isort:  ## To apply isort recursively
	poetry run isort $(APP)

.PHONY: fmt-black
fmt-black:  ## To get started black recursively
	poetry run black $(APP)

.PHONY: fmt
fmt: fmt-isort fmt-black

# === Tests ===

.PHONY: test
test:  ## Run tests
	poetry run pytest --verbose --capture=no --showlocals --durations=0

.PHONY: test-coverage
test-coverage: ## Run tests with coverage
	poetry run pytest --cov=$(APP) --cov-report=term --cov-report=html

# === Cache ===

.PHONY: clean
clean:  ## Clean up the cache folders
	@rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache .coverage coverage.xml htmlcov
	@echo "====> Cache folders deleted! \(^_^)/"
