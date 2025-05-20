# Use Python 3.12 slim image based on Debian Bookworm
FROM python:3.12-slim-bookworm

# Copy UV package manager from its official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy pyproject.toml first for better caching
COPY pyproject.toml .

# Install dependencies using UV
RUN uv sync

# Copy the rest of the application
COPY . .

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["uv", "run", "app.py"]