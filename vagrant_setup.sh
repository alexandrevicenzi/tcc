#!/usr/bin/env bash

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list

sudo apt-get update

sudo apt-get install -y mosquitto
sudo apt-get install -y mongodb-org
sudo apt-get install -y redis-server redis-tools

# sudo service mosquitto start
# sudo service mongod start
# sudo service redis-server start
