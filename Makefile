.EXPORT_ALL_VARIABLES:

APP = dosimeter
DOTENV_BASE_FILE ?= $(APP)/config/.env
TESTS = tests/**/*.py
POETRY_VERSION ?= 1.5.1

-include $(DOTENV_BASE_FILE)

# ==== Poetry ====

.PHONY: install-poetry
install-poetry:  ## Installation Poetry tool for dependency management and packaging in Python
	curl -sSL https://install.python-poetry.org | python3 - --version $(POETRY_VERSION)
	export PATH="$HOME/.local/bin"
	poetry --version

.PHONY: update-poetry
update-poetry:  ## Updating Poetry to the latest stable version
	poetry self update

.PHONY: where-is-my-venv
where-is-my-venv:  ## Showing the directory where the interpreter is installed
	poetry env info -p

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

.PHONY: tests-all
tests-all:  ## Run all tests
	poetry run pytest

.PHONY: tests
tests: ## Start tests only with specify markers option
	poetry run pytest --verbose --randomly-seed=default -m $(opt) --no-cov --disable-warnings

.PHONY: tests-coverage
tests-coverage: ## Run tests with coverage
	poetry run pytest --verbose --randomly-seed=default --cov=$(APP) --cov-report=term --cov-report=html

.PHONY: find-tests-slow
find-tests-slow: ## Find slow two tests
	poetry run pytest --verbose --randomly-seed=default --durations=3 --no-cov --disable-warnings

.PHONY: tests-slow
tests-slow: ## Start tests with 'slow' mark
	poetry run pytest --verbose --randomly-seed=default -m "slow" --no-cov --disable-warnings

.PHONY: tests-not-slow
tests-not-slow: ## Start quick tests (without 'slow' mark)
	poetry run pytest --verbose --randomly-seed=default -m "not slow" --no-cov --disable-warnings

# ==== Cache ====

.PHONY: clean
clean:  ## Clean up the cache folders
	@rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache coverage .coverage coverage.xml htmlcov
	@echo "====> Cache folders deleted! \(^_^)/"

# ==== Docker ====

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