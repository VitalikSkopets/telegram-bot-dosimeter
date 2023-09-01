FROM python:3.10

LABEL authors="vitaly.skopets"
LABEL maintainer="vitaly.skopets@itrexgroup.com"
LABEL vendor="itrexgroup.com"

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # poetry:
  POETRY_VERSION=1.5.1 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  PATH="/root/.local/bin:$PATH"

COPY poetry.lock pyproject.toml ./

RUN apt-get update  \
    && apt-get install --no-install-recommends -y curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION} \
    && poetry config virtualenvs._create false \
    && poetry install --no-root --without dev --no-interaction --no-ansi \
    # Cleaning cache:
    && rm -rf $(poetry config cache-dir)/{cache,artifacts} \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000