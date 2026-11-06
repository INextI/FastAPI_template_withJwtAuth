FROM python:3.14-slim

WORKDIR /backend

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY . .

RUN poetry run python main.py