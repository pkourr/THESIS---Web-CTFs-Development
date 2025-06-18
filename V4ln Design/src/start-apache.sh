#!/bin/bash
# Ensure permissions are set correctly
chmod 755 /var/www/html

# Check the Apache configuration for syntax errors
httpd -t

# Start Apache in the foreground
httpd -DFOREGROUND
