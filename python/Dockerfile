# syntax=docker/dockerfile:1

FROM amd64/python:3.10-slim-buster

# Install poetry
ENV POETRY_VERSION=1.5 \
    POETRY_VIRTUALENVS_CREATE=false
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry install --no-interaction --no-ansi --no-root --no-dev

# Copy Python code to the Docker image
COPY app /code/app/

ENV PYTHONPATH "${PYTHONPATH}:/app"