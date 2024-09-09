# Use an official Python runtime as a parent image
FROM python:3.11-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (using apk instead of apt-get for Alpine)
RUN apk update && apk add --no-cache \
    libpq-dev gcc python3-dev musl-dev postgresql-dev

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files into the container
COPY . /app/

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=core.settings
ENV DATABASE_URL=postgres://electro:electro@db:5432/electrodb

# Run makemigrations, migrate, and start the Gunicorn server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate &&  python manage.py collectstatic --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:8800"]
