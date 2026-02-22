FROM python:3.10-slim

# Install system dependencies (FFmpeg is required for video stitching)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create output directory
RUN mkdir -p output/clips

# Run the pipeline
CMD ["python", "main.py"]
