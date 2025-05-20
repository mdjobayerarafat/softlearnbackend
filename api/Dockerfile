# Use Python 3.12 slim image based on Debian Bookworm
FROM python:3.12-slim-bookworm

# Copy UV package manager from its official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Install dependencies using UV
RUN uv sync

# Run the application
CMD ["uv", "run", "app.py"]