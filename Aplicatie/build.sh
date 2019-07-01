#! /bin/bash

#set -e

if [ "$1" == "help" ]; then
  echo "./build.sh help      <-  help"
  echo "./build.sh first     <-  first run on machine"
  echo "./build.sh flask     <-  build flask-image and start docker-compose"
  echo "./build.sh emailer   <-  build emailer-image and start docker-compose"
  echo "./build.sh all       <-  build all images and start docker-compose"
  echo "./build.sh start     <-  start docker compose"
  echo "./build.sh stop      <-  stop docker compose"
  echo "./build.sh populate  <-  populate database tables"
  exit
fi

if [ "$1" != "populate" ]; then
  echo Exit Docker Swarm
  sudo docker swarm leave --force
  sleep 3
  if [ "$1" != "stop" ]; then
    echo Init Docker Swarm
    sudo docker swarm init
  fi
  sleep 3
fi

if [ "$1" == "first" ]; then
  # delete all containers
  sudo docker rm -f $(docker ps -a -q)

  sleep 1

  # delete all images
  sudo docker image rm -f $(docker images -q -a)

  # clean tree
  sudo rm -rf /var/lib/car-planner

  # create tree
  sudo mkdir /var/lib/car-planner
  sudo mkdir /var/lib/car-planner/registry
  sudo mkdir /var/lib/car-planner/mysql
  sudo mkdir /var/lib/car-planner/mysql-conf
  sudo mkdir /var/lib/car-planner/flask

  # copy application files
  sudo cp -R ./Flask/* /var/lib/car-planner/flask
  sudo cp -R ./MySQL/* /var/lib/car-planner/mysql-conf

  sleep 1
fi

if [ "$1" != "stop" ] && [ "$1" != "first" ]; then
  echo "Removing /var/lib/car-planner/flask/*"
  sudo rm -rf /var/lib/car-planner/flask/*
  echo "Removing /var/lib/car-planner/mysql-conf/*"
  sudo rm -rf /var/lib/car-planner/mysql-conf/*

  echo "Copying to /var/lib/car-planner/flask/*"
  sudo cp -R ./Flask/* /var/lib/car-planner/flask/
  echo "Copying to /var/lib/car-planner/mysql-conf/*"
  sudo cp -R ./MySQL/* /var/lib/car-planner/mysql-conf/
fi

if [ "$1" == "flask" ] || [ "$1" == "first" ]; then
  echo "Start building flask-image"
  sudo docker build --no-cache ./Dockerfiles -f ./Dockerfiles/FlaskDockerfile -t flask-image
fi

if [ "$1" == "emailer" ] || [ "$1" == "first" ]; then
  echo "Start building emailer-image"
  sudo docker build --no-cache ./Dockerfiles -f ./Dockerfiles/EmailerDockerfile -t emailer-image
fi

if [ "$1" == "all" ]; then
  echo "Start building flask-image"
  sudo docker build --no-cache ./Dockerfiles -f ./Dockerfiles/FlaskDockerfile -t flask-image
  echo "Start building emailer-image"
  sudo docker build --no-cache ./Dockerfiles -f ./Dockerfiles/EmailerDockerfile -t emailer-image
fi


if [ "$1" != "stop" ]; then
  sleep 1
  sudo docker stack deploy -c docker-compose.yml car-planner
fi

if [ "$1" == "stop" ]; then
  # delete all containers
  echo "Delete all containers"
  sudo docker rm -f $(docker ps -a -q)
fi

if [ "$1" == "populate" ]; then
  docker exec $(docker ps | grep flask | cut -d " " -f1 | head -1) python3 populateTables.py
fi
