FROM httpd:2.4.49-buster

# Create /var/www/html and set permissions
RUN mkdir -p /var/www/html && chmod 755 /var/www/html

# Copy the application's source code into the container
COPY ./httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ./html /var/www/html/
COPY ./flag.txt /var/www/html/flag.txt

# Copy the start script
COPY start-apache.sh /usr/local/bin/start-apache.sh

# Make sure the start script is executable
RUN chmod +x /usr/local/bin/start-apache.sh

# Use the custom script to start Apache
CMD ["/usr/local/bin/start-apache.sh"]
