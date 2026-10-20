FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create media/static directories and collect static
RUN mkdir -p media staticfiles
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

RUN python manage.py migrate --noinput || true
# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
