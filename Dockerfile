# Use official lightweight Python image,
FROM python:3.11-slim

# Set working directory inside container,
WORKDIR /app

# Install apt packages (if needed later),
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching),
COPY requirements.txt .

# Install Python dependencies,
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project,
COPY . .

# Default run command (Railway overrides this),
CMD ["python", "bot.py"]