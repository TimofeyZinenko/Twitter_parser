FROM python:3.10 as builder

RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.prod.txt  .
# hadolint ignore=DL3013, DL3008
RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --wheel-dir ./wheels -r requirements.prod.txt

# Финальный этап
FROM python:3.10-slim
WORKDIR /app


COPY --from=builder /app/wheels/ /wheels
COPY --from=builder /app/requirements.prod.txt .
# hadolint ignore=DL3008,DL3013
RUN apt-get update && \
    apt-get --no-install-recommends install -y netcat && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install  --no-cache-dir --no-cache /wheels/*
COPY /app/ .
