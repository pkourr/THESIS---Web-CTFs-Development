FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_PORT 4242

# Setup the application directory
WORKDIR /usr/src/app
# Copy the application files to the container
COPY ./app /usr/src/app
# Install dependencies defined in the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt
# Expose the application's port
EXPOSE 4242
# Make the server script executable
RUN chmod +x /usr/src/app/serve.sh
# Command to run the application
CMD ["./serve.sh"]


