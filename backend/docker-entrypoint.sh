#!/bin/sh
set -e

DATA_DIR=$(dirname "$DATA_PATH")
mkdir -p "$DATA_DIR"

if [ ! -f "$DATA_PATH" ]; then
  echo "[entrypoint] generating synthetic data..."
  python /tmp/generate_synthetic.py "$DATA_PATH"
fi

if [ ! -f "$DB_PATH" ]; then
  echo "[entrypoint] running ETL..."
  python -m app.etl.run
fi

exec "$@"
