FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_PORT 4242

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the application directory contents into the container at /usr/src/app
COPY ./app /usr/src/app

# Install the dependencies defined in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application's port
EXPOSE 4242

# Copy the serve.sh script into the container
COPY ./app/serve.sh /usr/src/app

# Give execution rights on scripts
RUN chmod +x /usr/src/app/serve.sh

# Initialize the database and then start the Flask app
CMD python3 -c 'from app import create_users_table; create_users_table()' && ./serve.sh


