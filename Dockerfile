FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system dependencies and cleanup in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    netcat-traditional \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Create necessary directories
RUN useradd -m appuser && \
    mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

EXPOSE 8000

# Combined initialization and startup command
CMD set -e; \
    echo "Waiting for database..."; \
    until nc -z -v -w30 db 3306; do \
        echo "Waiting for database connection..."; \
        sleep 5; \
    done; \
    echo "Running migrations..."; \
    python manage.py migrate --noinput; \
    echo "Collecting static files..."; \
    python manage.py collectstatic --noinput; \
    echo "Starting Gunicorn..."; \
    exec gunicorn \
        --bind 0.0.0.0:8000 \
        core.wsgi:application \
        --workers 3 \
        --timeout 120 \
        --keep-alive 5 \
        --max-requests 1000 \
        --max-requests-jitter 50