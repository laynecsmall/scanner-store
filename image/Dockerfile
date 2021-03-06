############################################################
# Dockerfile to build apache-flask container images
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Layne Small

# Update the repository sources list
RUN apt-get update

################## BEGIN INSTALLATION ######################

# Add the package verification key
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

# Update the repository sources list once more
RUN apt-get update
RUN apt-get -y upgrade

# Install Apache2
RUN apt-get install -y \
	apache2 \
	apache2-utils \
	libapache2-mod-wsgi \
	git  \
  python-pip \
  python-dev \
  vim \
  build-essential \
  libsqlite3-dev \
  sqlite3

# Create the default directory
RUN mkdir -p /srv/www
RUN mkdir -p /srv/db
RUN chown www-data /srv/db 
RUN chmod 775 /srv/db

# Clone the app from github and install packages
RUN git clone https://github.com/laynecsmall/scanner-store /srv/www/app
RUN cp -f /srv/www/app/apache/config/default.conf /etc/apache2/sites-available/000-default.conf
RUN pip install -r /srv/www/app/requirements.txt 

##################### INSTALLATION END #####################

# Expose the default port
EXPOSE 80

# Set default container command
ENTRYPOINT /usr/sbin/apache2ctl -D FOREGROUND
