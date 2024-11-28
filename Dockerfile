# Use a base Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Reflex CLI globally
RUN pip install reflex-cli

# Copy your project files to the container
COPY . .

# Install project dependencies
RUN pip install -r requirements.txt

# Expose the Reflex default port
EXPOSE 3000 8000

# Run the Reflex app
CMD ["reflex", "run"]
