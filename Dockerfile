# ── Stage 1: Base ──────────────────────────
FROM python:3.12-slim AS base

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ── Stage 2: Dependencies ─────────────────
FROM base AS dependencies

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Stage 3: Application ──────────────────
FROM dependencies AS application

COPY . .

# Ensure production settings are used in container runtime commands.
ENV DJANGO_SETTINGS_MODULE=config.settings.production

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/media

# Collect static files (will be served by whitenoise)
RUN python manage.py collectstatic --noinput --settings=config.settings.production 2>/dev/null || true

# Create non-root user for security
RUN addgroup --system django && \
    adduser --system --ingroup django django && \
    chown -R django:django /app

USER django

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')" || exit 1

# Default command: migrate first, then run ASGI server.
CMD ["sh", "-c", "python manage.py migrate --no-input && daphne -b 0.0.0.0 -p ${PORT:-8000} config.asgi:application"]
