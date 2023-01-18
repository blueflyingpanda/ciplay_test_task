FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install the dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN pip install --no-cache-dir -r requirements.txt


# Copy the application code
COPY . .

CMD uvicorn main:app --host 0.0.0.0 --port ${API_PORT}