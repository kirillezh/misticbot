# Use a compatible base image
FROM python:3.9-bullseye

# Install required tools and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    gnupg \
    ca-certificates \
    unzip \
    ffmpeg \
    chromium \
    chromium-driver && \
    rm -rf /var/lib/apt/lists/*

# Set Chromium as the default browser
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromedriver

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV DISPLAY=:99
ENV APP_HOME /app

# Set working directory
WORKDIR ${APP_HOME}

# Copy application files
COPY . .

# Set entry point and command
ENTRYPOINT ["python3"]
CMD ["main.py"]
