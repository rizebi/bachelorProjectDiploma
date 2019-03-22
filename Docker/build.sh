#! /bin/bash

#set -e

if [ "$1" == "help" ]; then
  echo "./build.sh help     <-  help"
  echo "./build.sh first    <-  first run on machine"
  echo "./build.sh flask    <-  build flask-image and start docker-compose"
  echo "./build.sh emailer  <-  build emailer-image and start docker-compose"
  echo "./build.sh start    <-  start docker compose"
  echo "./build.sh          <-  start docker compose"
  echo "./build.sh stop     <-  stop docker compose"
  exit
fi



echo Exit Docker Swarm
sudo docker swarm leave --force
echo Init Docker Swarm
sudo docker swarm init
echo Stopping the containers
sudo docker stack rm car-planner

if [ "$1" == "first" ]; then
  sudo mkdir /var/lib/car-planner
  sudo mkdir /var/lib/car-planner/registry
  sudo mkdir /var/lib/car-planner/mysql
  sudo mkdir /var/lib/car-planner/flask
  sudo mkdir /var/lib/car-planner/emailer

  sudo cp ./Flask_Docker/app.py /var/lib/car-planner/flask
  sudo cp ./Emailer_Docker/app.py /var/lib/car-planner/emailer
fi

if [ "$1" == "flask" ] || [ "$1" == "first" ]; then
  sudo docker build --no-cache . -f ./Flask_Docker/FlaskDockerfile -t flask-image
fi

if [ "$1" == "emailer" ] || [ "$1" == "first" ]; then
  sudo docker build --no-cache . -f ./Emailer_Docker/EmailerDockerfile -t emailer-image

fi

if [ "$1" != "stop" ]; then
  sudo docker stack deploy -c docker-compose.yml car-planner
fi
