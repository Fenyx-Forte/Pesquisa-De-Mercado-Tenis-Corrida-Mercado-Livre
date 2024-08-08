# The builder image, used to build the virtual environment
FROM python:3.12-bookworm as builder

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.3 python3 -

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN /root/.local/bin/poetry install --without docs,jupyter,dev,testes,webscraping --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.12-slim-bookworm as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src ./src

# COPY config ./config

# COPY dados ./dados

# COPY sql . sql

WORKDIR /src

EXPOSE 8501
ENTRYPOINT ["task", "run-streamlit"]
