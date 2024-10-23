# Use the official Python image (version 3.12)
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (gcc, libc, etc.) required for compiling Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of application's code to the container
COPY . .

# Command to run your bot
CMD ["python", "main.py"]
