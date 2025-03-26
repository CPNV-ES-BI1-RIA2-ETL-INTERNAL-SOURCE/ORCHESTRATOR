FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends iputils-ping \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock /app/

ENV PIPENV_CUSTOM_VENV_NAME=ORCHESTRATOR
RUN pip install --no-cache-dir pipenv && pipenv install --deploy --ignore-pipfile

COPY . /app

RUN pipenv run pytest

EXPOSE 8000

CMD ["pipenv", "run", "fastapi", "run"]