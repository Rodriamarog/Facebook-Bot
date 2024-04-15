# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y locales procps wget unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up the locale
RUN locale-gen es_MX.UTF-8

# Set locale environment variables
ENV LANG es_MX.UTF-8
ENV LANGUAGE es_MX:es
ENV LC_ALL es_MX.UTF-8

# Set the timezone
ENV TZ=America/Tijuana
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Upgrade pip
RUN pip install --upgrade pip

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install \
    && rm google-chrome-stable_current_amd64.deb

# Install ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/bin/chromedriver \
    && chown root:root /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm chromedriver_linux64.zip

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot script
CMD ["python", "post_to_facebook.py"]
