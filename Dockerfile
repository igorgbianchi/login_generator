FROM python:3.9.4-slim

RUN pip install -U pip

RUN apt update -y && \
    apt install --no-install-recommends -y \
    build-essential && \
    rm -rf /var/cache/apt/* /var/lib/apt/lists/*

ENV POETRY_VERSION=1.2.1

RUN pip install "poetry==$POETRY_VERSION"
RUN pip install virtualenv

COPY pyproject.toml poetry.lock /tmp/
WORKDIR /tmp
RUN poetry export --without-hashes --with-credentials --no-interaction --no-ansi -f requirements.txt -o requirements.txt && \
    python -m venv /venv && \
    /venv/bin/pip install --force-reinstall -r requirements.txt && \
    rm -rf pyprojects.toml poetry.lock requirements.txt

COPY ./src /app

ENV PATH="/venv/bin:$PATH"

WORKDIR /app/

ENTRYPOINT ["python", "app.py"]