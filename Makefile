.EXPORT_ALL_VARIABLES:

SHELL  := $(shell which zsh)
PYTHON := $(shell which python3)
POETRY := $(shell which poetry)

APP            = dosimeter
TESTS          = ./tests/**/*.py
ENV_FILE       = ./$(APP)/config/.env
DEPS_FILE      = ./requirements.txt
POETRY_VERSION = 1.8.4

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

.PHONY: check
check:  ## Validate the content of the pyproject.toml and its consistency with the poetry.lock
	@$(POETRY) check

.PHONY: venv-info
venv-info:  ## Get basic information about the currently activated virtual environment
	@$(POETRY) env info

.PHONY: where-is-my-venv
where-is-my-venv:  ## Get the path to the virtual environment
	@$(POETRY) env info -path

.PHONY: where-is-my-python
where-is-my-python:  ## Get the path to the python executable
	@$(POETRY) env info --executable

# ====================================
#        Manage Dependencies
# ====================================

.PHONY: list-deps
list-deps:  ## Show list all the available packages
	@$(POETRY) show

.PHONY: show-details
show-details:  ## Check the details of a certain package
ifdef package
	@$(POETRY) show $(package)
endif
ifndef package
	$(warning WARNING: Please provide a package name.)
	$(error You must usage command: 'make show-details package=<package_name>')
endif

.PHONY: compare-deps
compare-deps:  ## Compare locked dependencies against their latest releases on PyPI
	@$(POETRY) show --latest --top-level

.PHONY: update-all-deps
update-all-deps:  ## Update all packages along with their dependencies to their latest compatible versions
	@$(POETRY) update

.PHONY: update-deps-dry-run
update-deps-dry-run:  ## Show which dependencies will be updated and in which direction
	@$(POETRY) update --dry-run

.PHONY: update-deps
update-deps:  ## Update one specific package
ifdef package
	@$(POETRY) update $(package)
endif
ifndef package
	$(warning WARNING: Please provide a package name.)
	$(error You must usage command 'make update package=<package_name>')
endif

.PHONY: export-deps
export-deps:  ## Export dependencies from poetry into requirements.txt
	@$(POETRY) run $(PYTHON) -m pip freeze > $(DEPS_FILE)
	$(info All dependency packages have been exported to a file '$(DEPS_FILE)' successfully!)

# ====================================
#             Launch App
# ====================================

HONY: load-env
load-env:  ## Load environment variables before launch app
	export $(shell grep -v '^#' $(ENV_FILE) | xargs) && $(SHELL)
	$(info Environment variables from the file '$(ENV_FILE)' have been uploaded successfully!)


.PHONY: run
run: load-env  ## Run main function in main.py file - entry point in app
	@$(POETRY) run main-run

# ====================================
#         Linters and formating
# ====================================

.PHONY: lint
lint:  ## Lint and static-check
	$(info Checking started...)
	$(POETRY) run isort --check-only --diff $(APP)
	$(POETRY) run black --check --diff $(APP)
	$(POETRY) run ruff $(APP)
	$(POETRY) run mypy $(APP) $(TESTS) --show-error-codes
	$(POETRY) run yamllint -d '{"extends": "default", "ignore": ".venv"}' -s .
	$(info The linter, style, and ctatic check has been completed successfully!)

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
clean:  ## Clean up the cache folders and recursively find and delete all __pycache__ directories
	@rm -rf .DS_Store .pytest_cache .mypy_cache .ruff_cache coverage .coverage coverage.xml htmlcov
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	$(info Directories with cache files have been successfully deleted!)

.PHONY: cache-list
cache-list:  ## Lists Poetry’s available caches
	@$(POETRY) cache list

.PHONY: cache-clear
cache-clear:  ## Clear the whole cache of packages from a cached repository
ifdef repo
	@$(POETRY) cache clear $(repo) --all
endif
ifndef repo
	$(warning WARNING: Please provide a cached repository name.)
	$(error You must usage command 'make cache-clear repo=<repository_name>')
endif

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