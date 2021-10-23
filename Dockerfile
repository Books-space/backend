FROM debian:stable-slim AS unzip

WORKDIR /books

RUN apt-get update && apt-get install unzip && \
        apt-get clean autoclean && \
        apt-get autoremove --yes && \
        rm -rf /var/lib/{apt,dpkg,cache,log}/
COPY books.csv.zip .
RUN unzip books.csv.zip
RUN rm books.csv.zip


FROM python:3.9.7-slim-bullseye AS final

WORKDIR /backend

COPY pyproject.toml poetry.lock /backend/
RUN pip install "poetry==1.1.0"
RUN pip install --upgrade pip
RUN poetry config virtualenvs.create false && poetry install

COPY --from=unzip /books/books.csv /backend/

COPY webapp/ /backend/

ENTRYPOINT ["python", "main.py"]
