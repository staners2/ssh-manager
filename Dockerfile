FROM duffn/python-poetry:3.10.8-slim-1.6.1

ENV LANGUAGE ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false && poetry install -vvv --only main
