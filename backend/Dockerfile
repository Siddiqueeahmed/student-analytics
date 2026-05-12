FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (layer-cached until pyproject.toml changes)
COPY backend/pyproject.toml .
RUN pip install --no-cache-dir hatchling && \
    pip install --no-cache-dir polars fastapi "uvicorn[standard]" python-dotenv

# Generate synthetic data into the image so the container is self-contained
COPY data/generate_synthetic.py ./data/generate_synthetic.py
RUN python data/generate_synthetic.py

# Copy application source
COPY backend/app ./app

ENV DATA_PATH=/app/data/students.csv

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
