#!/bin/bash

# initiate the scraping
python3.5 audiophile.py

# start apache
/etc/init.d/apache2 start

# start gunicorn and flask
gunicorn -b 127.0.0.1:5000 app:app
