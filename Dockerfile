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

# Create necessary directories with proper permissions
RUN useradd -m appuser && \
    mkdir -p /app/staticfiles/img /app/staticfiles/css /app/staticfiles/js /app/media && \
    chown -R appuser:appuser /app && \
    chmod -R 775 /app/staticfiles

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY --chown=appuser:appuser . .

# Collect static files before switching user
RUN python manage.py collectstatic --noinput

# Switch to non-root user
USER appuser

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

EXPOSE 8000

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Waiting for database...";\n\
until nc -z -v -w30 $DB_HOST $DB_PORT; do\n\
    echo "Waiting for database connection...";\n\
    sleep 5;\n\
done;\n\
echo "Running migrations...";\n\
python manage.py migrate --noinput;\n\
echo "Starting Gunicorn...";\n\
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 50' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]