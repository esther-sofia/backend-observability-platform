# Use a stable slim Python image
FROM python:3.11-slim

# Prevents python from writing .pyc and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps for psycopg build and common libs
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt /app/

# Upgrade pip and install python deps (including psycopg binary wheel if present)
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app

# Expose port
EXPOSE 8000

# Default command (overridden by docker-compose command if present)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
