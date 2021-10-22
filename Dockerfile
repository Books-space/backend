FROM python:3.9.7-slim-bullseye

RUN mkdir /backend

WORKDIR /backend

COPY pyproject.toml poetry.lock /backend/

RUN pip install "poetry==1.1.0"

RUN pip install --upgrade pip

RUN poetry config virtualenvs.create false && poetry install

COPY webapp /backend/

ENTRYPOINT ["python", "-m", "webapp"]