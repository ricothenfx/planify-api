FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files
COPY backend/pyproject.toml backend/uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY backend/ .

EXPOSE 8000

# Run migrations then start server
CMD uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000