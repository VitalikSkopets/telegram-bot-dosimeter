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
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.5.1 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  PATH="${PATH}:$HOME/.local/bin"

COPY poetry.lock pyproject.toml ./

RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install poetry==${POETRY_VERSION} \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --without dev --no-interaction --no-ansi \
    # Cleaning cache:
    && rm -rf $(poetry config cache-dir)/{cache,artifacts} \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000