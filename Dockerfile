# Sử dụng Python slim image cho crypto bot
FROM python:3.10-slim

# Install system dependencies cần thiết cho crypto analysis
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first để tận dụng Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Health check để kiểm tra bot hoạt động
HEALTHCHECK --interval=60s --timeout=30s --start-period=10s --retries=3 \
    CMD python -c "import requests; requests.get('https://api.binance.com/api/v3/ping', timeout=10)" || exit 1

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Ho_Chi_Minh

# Expose port (required for Cloud Run)
EXPOSE 8080

# Run crypto alert bot
CMD ["python", "main.py"]
