# Use Python 3.9 slim image
FROM python:3.9-slim

# Install system dependencies for OCR and supported languages
# This includes Tesseract, GCC/G++, Java, Node.js, Go, Ruby, and R
# Note: Kotlin is not always available in default apt repos or requires manual install, 
# so we install what is easily available. 
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    g++ \
    gcc \
    default-jdk \
    nodejs \
    golang-go \
    ruby-full \
    r-base \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Environment variable for Tesseract is not needed as it's in PATH, 
# but we can set it if necessary.
# ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

# Hugging Face Spaces run on port 7860 by default
EXPOSE 7860

# Command to run the application
CMD ["python", "app.py"]
