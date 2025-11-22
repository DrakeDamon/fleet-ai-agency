FROM python:3.10-slim

WORKDIR /code

# Copy requirements first for better caching
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the entire app directory
COPY ./app /code/app

# Render automatically sets the PORT env var
# Default to 8000 if PORT is not set (for local development)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
