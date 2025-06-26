# messaging_app/Dockerfile
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements.txt from the root of messaging_app/
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full Django project
COPY . .

# Open port 8000
EXPOSE 8000

# Start Django server using correct settings path
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000", "--settings=messaging_app.settings"]
