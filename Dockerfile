FROM python:3.9.7-slim-bullseye

WORKDIR /backend

COPY pyproject.toml poetry.lock /backend/

RUN pip install "poetry==1.1.0" && \
    pip install --upgrade pip && \
    poetry config virtualenvs.create false && \
    poetry install

COPY webapp /backend/webapp

CMD ["python", "-m", "webapp"]