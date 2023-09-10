# syntax=docker/dockerfile:1


#ARG PYTHON_VERSION=3.9
#FROM python:${PYTHON_VERSION}-slim as base
FROM pytorch/pytorch:latest

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install poetry environment
RUN pip3 install poetry

RUN apt-get update
RUN apt-get install build-essential -y

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# Copy sourcecode to docker env
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
#CMD uvicorn 'main:app' --host=127.0.0.1 --port=8000
CMD [ "poetry", "run", "python3", "main.py" ]
