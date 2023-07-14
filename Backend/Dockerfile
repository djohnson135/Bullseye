FROM python:3.10.0 as python-base

ARG APP_NAME=bullseye_backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    POETRY_VERSION=1.4.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /opt/code
COPY ./poetry.lock ./pyproject.toml README.md ./
COPY ./$APP_NAME ./$APP_NAME

RUN poetry install

EXPOSE 8000
EXPOSE 443
EXPOSE 80
CMD ["poetry", "run", "start"]