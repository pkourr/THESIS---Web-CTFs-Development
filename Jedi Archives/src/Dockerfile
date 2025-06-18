# Use HAProxy as the base image
FROM haproxy:2.2.16

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_PORT 4242

# Install dependencies required for building Python 3.8.10 from source
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    zlib1g-dev \
    liblzma-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    && rm -rf /var/lib/apt/lists/*

# Download, compile, and install Python 3.8.10
RUN curl -O https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tar.xz \
    && tar -xf Python-3.8.10.tar.xz \
    && cd Python-3.8.10 \
    && ./configure --enable-optimizations \
    && make -j 8 \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.8.10.tar.xz Python-3.8.10

# Install pip for Python 3.8
RUN curl -O https://bootstrap.pypa.io/get-pip.py \
    && python3.8 get-pip.py \
    && rm get-pip.py

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the image
COPY ./app/requirements.txt /app/requirements.txt
# config-backup.txt is in the src/app directory
COPY ./app/config-backup.txt /app/config-backup.txt


# Install python requirements
RUN pip install -r requirements.txt --no-cache-dir

# Copy the Flask application and HAProxy configuration
COPY ./app /app
COPY ./config/haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg

# Copy and grant execution permissions to the serve script
COPY ./app/serve.sh /serve.sh
RUN chmod +x /serve.sh

# Expose the application's port
EXPOSE 8081 80 4242

# Start the services using the script
CMD ["/bin/sh", "/app/serve.sh"]



