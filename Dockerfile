FROM python:3.12-slim

WORKDIR /app

# Copy uv binary from the official distroless Docker image
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /uvx /bin/

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies - this layer will be cached as long as pyproject.toml and uv.lock don't change
RUN uv pip install --system ".[test]"

# Copy the rest of the application
COPY src/ src/
COPY tests/ tests/
COPY pytest.ini ./

RUN uv pip install --system .

EXPOSE 8000

CMD ["python", "src/main.py"]
