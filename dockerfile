# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG es_MX.UTF-8
ENV LANGUAGE es_MX:es
ENV LC_ALL es_MX.UTF-8
ENV TZ=America/Tijuana

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    locales \
    procps \
    wget \
    unzip \
    curl \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    --no-install-recommends \
    && echo "es_MX.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Upgrade pip
RUN pip install --upgrade pip

# Install Google Chrome
RUN wget -q -O /tmp/chrome-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.122/linux64/chrome-linux64.zip \
    && unzip /tmp/chrome-linux64.zip -d /opt/chrome \
    && ls -la /opt/chrome \
    && rm /tmp/chrome-linux64.zip

# Ensure Google Chrome is installed correctly
RUN ln -s /opt/chrome/chrome-linux64/chrome /usr/bin/google-chrome

# Install ChromeDriver
RUN wget -q -O /tmp/chromedriver-linux64.zip "https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.122/linux64/chromedriver-linux64.zip" \
    && unzip /tmp/chromedriver-linux64.zip -d /tmp/chromedriver/ \
    && ls -la /tmp/chromedriver/ \
    && mv /tmp/chromedriver/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -r /tmp/chromedriver/ \
    && rm /tmp/chromedriver-linux64.zip


# Verify ChromeDriver installation
RUN chromedriver --version

ENV PATH $PATH:/usr/local/bin/chromedriver

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot script
CMD ["python", "post_to_facebook.py"]
