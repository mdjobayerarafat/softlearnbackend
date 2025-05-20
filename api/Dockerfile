FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --frozen

COPY requirements.txt .
COPY requirements.lock .

# Copy the rest of the application
COPY . .

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1
# Run the application
CMD ["uv", "run", "app.py"]