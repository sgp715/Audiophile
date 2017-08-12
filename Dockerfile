FROM ubuntu


RUN apt-get update && apt-get install -y

RUN apt-get install nano -y

# install Apache
RUN apt-get install apache2 -y
RUN echo "proxy proxy_ajp proxy_http rewrite deflate headers proxy_balancer proxy_connect proxy_html" | a2enmod

# add our config for the app
RUN rm /etc/apache2/sites-enabled/000-default.conf
COPY 000-default.conf /etc/apache2/sites-enabled/


# setting up flask app
WORKDIR /app
COPY app /app

RUN echo '{"key":"10d3d179c39948718d579dd04cda0c61"}' > config.json
RUN echo "{}" > metadata.json

# start up the gunicorn server
#   RUN start.sh


# install python and requirements
RUN apt-get install python3.5 -y
RUN apt-get install python3-pip -y
RUN pip3 install -r requirements.txt

# add the cronjob
RUN apt-get install cron
RUN crontab cron

# start flask
RUN chmod +x start.sh
ENTRYPOINT ./start.sh
