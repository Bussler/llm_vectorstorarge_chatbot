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
ARG HUGGINGFACE_ACCESS_TOKEN
ENV HUGGINGFACE_TOKEN=$HUGGINGFACE_ACCESS_TOKEN
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
#CMD [ "poetry", "run", "python3", "main.py" ]
