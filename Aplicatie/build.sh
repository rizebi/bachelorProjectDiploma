#! /bin/bash

#set -e

if [ "$1" == "help" ]; then
  echo "./build.sh help     <-  help"
  echo "./build.sh first    <-  first run on machine"
  echo "./build.sh flask    <-  build flask-image and start docker-compose"
  echo "./build.sh emailer  <-  build emailer-image and start docker-compose"
  echo "./build.sh all      <-  build all images and start docker-compose"
  echo "./build.sh start    <-  start docker compose"
  echo "./build.sh stop     <-  stop docker compose"
  echo "./build.sh copy     <-  copy the files to /var/lib/car-planner/X"
  exit
fi

if [ "$1" == "copy" ]; then
  echo "Removing /var/lib/car-planner/flask/*"
  sudo rm -rf /var/lib/car-planner/flask/*
  echo "Removing /var/lib/car-planner/emailer/*"
  sudo rm -rf /var/lib/car-planner/emailer/*
  echo "Copying to /var/lib/car-planner/flask/*"
  sudo cp -R ./Flask/* /var/lib/car-planner/flask/
  echo "Copying to /var/lib/car-planner/emailer/*"
  sudo cp -R ./Emailer/* /var/lib/car-planner/emailer/
  exit
fi

echo Exit Docker Swarm
sudo docker swarm leave --force
if [ "$1" != "stop" ]; then
  echo Init Docker Swarm
  sudo docker swarm init
fi

if [ "$1" == "first" ]; then
  # delete all containers
  sudo docker rm -f $(docker ps -a -q)

  # delete all images
  sudo docker image rm -f $(docker images -q -a)

  # clean tree
  sudo rm -rf /var/lib/car-planner

  # create tree
  sudo mkdir /var/lib/car-planner
  sudo mkdir /var/lib/car-planner/registry
  sudo mkdir /var/lib/car-planner/mysql
  sudo mkdir /var/lib/car-planner/flask
  sudo mkdir /var/lib/car-planner/emailer

  # copy application files
  sudo cp ./Flask/* /var/lib/car-planner/flask
  sudo cp ./Emailer/* /var/lib/car-planner/emailer
fi

if [ "$1" == "flask" ] || [ "$1" == "first" ]; then
  echo "Start building flask-image"
  docker build --no-cache ./Dockerfiles -f ./Dockerfiles/FlaskDockerfile -t flask-image
fi

if [ "$1" == "emailer" ] || [ "$1" == "first" ]; then
  echo "Start building emailer-image"
  docker build --no-cache ./Dockerfiles -f ./Dockerfiles/EmailerDockerfile -t emailer-image
fi

if [ "$1" == "all" ]; then
  echo "Start building flask-image"
  docker build --no-cache ./Dockerfiles -f ./Dockerfiles/FlaskDockerfile -t flask-image
  echo "Start building emailer-image"
  docker build --no-cache ./Dockerfiles -f ./Dockerfiles/EmailerDockerfile -t emailer-image
fi


if [ "$1" != "stop" ]; then
  sudo docker stack deploy -c docker-compose.yml car-planner
fi