FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_PORT 4242

# Install MongoDB
RUN apt-get update && \
    apt-get install -y gnupg wget && \
    wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add - && \
    echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list && \
    apt-get update && \
    apt-get install -y mongodb-org && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create MongoDB data directory
RUN mkdir -p /data/db

# Setup the application directory
RUN mkdir -p /opt/app
# Copy the application files to the container
COPY app/ /opt/app/
WORKDIR /opt/app

# Install dependencies defined in the requirements.txt file
RUN pip install -r requirements.txt --no-cache-dir

# Expose the application's port
EXPOSE 4242

# Define the command to run MongoDB and then start the Flask application
CMD mongod --fork --logpath /var/log/mongod.log; cat /var/log/mongod.log; /bin/sh /opt/app/serve.sh
