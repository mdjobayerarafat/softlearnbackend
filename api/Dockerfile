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

# Copy only the API directory content
COPY api/ /app/

# Create content directory for static files
RUN mkdir -p content

# Install dependencies using UV
RUN uv pip install --system \
    boto3>=1.34.79 \
    botocore>=1.34.93 \
    faker>=30.1.0 \
    fastapi>=0.115.0 \
    fastapi-jwt-auth>=0.5.0 \
    httpx>=0.27.0 \
    langchain>=0.1.7 \
    langchain-community>=0.0.20 \
    langchain-openai>=0.0.6 \
    openai>=1.50.2 \
    passlib>=1.7.4 \
    psycopg2-binary>=2.9.9 \
    "pydantic[email]>=1.8.0,<2.0.0" \
    pytest>=8.2.2 \
    python-dotenv>=1.0.0 \
    python-multipart>=0.0.9 \
    pyyaml>=6.0.1 \
    redis>=5.0.7 \
    requests>=2.32.3 \
    resend>=2.4.0 \
    sqlmodel>=0.0.19 \
    tiktoken>=0.7.0 \
    uvicorn==0.30.1 \
    typer>=0.12.5 \
    chromadb==0.5.16 \
    alembic>=1.13.2 \
    alembic-postgresql-enum>=1.2.0 \
    sqlalchemy-utils>=0.41.2 \
    stripe>=11.1.1 \
    python-jose>=3.3.0 \
    "logfire[sqlalchemy]>=3.8.0"


# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose the port FastAPI runs on
EXPOSE 8000

# Start the FastAPI application with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]