FROM python:3.13-alpine AS builder

WORKDIR /service

COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir --no-input pipenv
RUN pipenv install --system --deploy

# Test
FROM builder AS test
WORKDIR /service

COPY tests ./tests

RUN pipenv install --system --deploy --dev
RUN python -m pytest

# Runtime
FROM python:3.13-alpine AS runtime

RUN apk add --no-cache poppler-utils

WORKDIR /service

RUN mkdir /service/.venv

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY main.py ./
COPY app ./app

COPY config ./config

EXPOSE 8000

CMD ["python", "-m", "fastapi", "run", "main.py", "--port", "8000"]