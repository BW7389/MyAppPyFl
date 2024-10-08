# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables to prevent Python from generating .pyc files and to ensure stdout/stderr are unbuffered
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=main.py

# Create a non-root user and switch to it
RUN adduser --disabled-password appuser
USER appuser

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
