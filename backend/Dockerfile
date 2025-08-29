FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set workdir to /app for dependency install
WORKDIR /app

# System deps (psycopg, build tools)
RUN apt-get update && apt-get install -y \
    build-essential curl libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# --- Install deps ---
# Use requirements.txt for speed in CI; pyproject.toml for modern workflows
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# App source
COPY . /app

# Set proper PYTHONPATH
ENV PYTHONPATH=/app

# Switch to app dir for running
WORKDIR /app

EXPOSE 8000

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Healthcheck endpoint: /health
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
