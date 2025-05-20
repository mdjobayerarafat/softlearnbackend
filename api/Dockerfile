# Use Python 3.12 slim image based on Debian Bookworm
FROM python:3.12-slim-bookworm

# Install system dependencies required for psycopg2 and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy UV package manager from its official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy entire project first
COPY . .

# Install Python dependencies using UV
RUN uv pip install --system hatchling && \
    uv pip install --system .

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose the port FastAPI runs on
EXPOSE 8000

# Start the FastAPI application with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]