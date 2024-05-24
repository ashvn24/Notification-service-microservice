# Build stage
FROM python:3.12-slim AS builder


WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.12-slim AS production

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

COPY --from=builder /app /app

ENV PYTHONUNBUFFERED=1


EXPOSE 8001

