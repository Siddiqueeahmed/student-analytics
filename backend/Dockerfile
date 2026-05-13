FROM python:3.11-slim

WORKDIR /app

# Install dependencies from pyproject.toml
COPY backend/pyproject.toml ./pyproject.toml
RUN pip install --no-cache-dir hatchling && \
    pip install --no-cache-dir \
        fastapi "uvicorn[standard]" polars python-dotenv duckdb \
        pydantic-settings cachetools structlog \
        "python-jose[cryptography]" "passlib[bcrypt]" python-multipart \
        slowapi prometheus-client \
        opentelemetry-sdk opentelemetry-instrumentation-fastapi \
        opentelemetry-exporter-otlp-proto-grpc

# Generate synthetic data and run ETL so the DB exists at startup
COPY data/generate_synthetic.py ./data/generate_synthetic.py
COPY backend/app ./app

ENV DATA_PATH=/app/data/students.csv \
    DB_PATH=/app/data/analytics.duckdb

RUN python data/generate_synthetic.py "$DATA_PATH" && \
    python -m app.etl.run

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
