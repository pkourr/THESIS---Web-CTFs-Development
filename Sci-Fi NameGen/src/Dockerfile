FROM php:7.0-apache

# Copy your application source code to the image
COPY html/ /var/www/html/

# Copy the flag into the container
COPY flag.txt /var/www/

# Modify permissions to make the flag file readable by the web server
RUN chmod a+r /var/www/flag.txt

# Expose port 80
EXPOSE 80


