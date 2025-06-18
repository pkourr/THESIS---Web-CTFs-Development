FROM php:7.2.12-apache

# Copy application's source code to the image
COPY html/ /var/www/html/

# Create and set proper permissions for the uploads directory
RUN mkdir -p /var/www/html/uploads && chown -R www-data:www-data /var/www/html/uploads

# Copy the flag file into the root directory of the container
COPY flag.txt /
# Make the flag file readable to everyone.
RUN chmod a+r /flag.txt

# Expose port 80
EXPOSE 80