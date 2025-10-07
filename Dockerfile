FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libjpeg-dev \
    zlib1g-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    poppler-utils \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt requirements.txt

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy rest of the app
COPY . .

# Expose port if your app serves requests
EXPOSE 8080

CMD ["python", "app.py"]
