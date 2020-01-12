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
  echo "./build.sh push      <-  tag and push images to private docker registry"
  echo "./build.sh pull      <-  pull and tag images from private docker registry"
  echo "./build.sh images    <-  query private docker registry for existing images"
  echo "./build.sh daily     <-  send daily notification emails"
  echo "./build.sh weekly    <-  send weekly notification emails"
  exit
fi

if [ "$1" == "populate" ]; then
  docker exec $(docker ps | grep flask | cut -d " " -f1 | head -1) python3 populateTables.py

  exit
fi

if [ "$1" == "push" ]; then
  sudo docker image rm localhost:444/flask-image
  sudo docker image rm localhost:444/emailer-image
  sudo docker image rm localhost:444/mysql:5.7
  sudo docker image rm localhost:444/alpine
  sudo docker image rm localhost:444/prometheus


  sudo docker tag flask-image localhost:444/flask-image
  sudo docker tag emailer-image localhost:444/emailer-image
  sudo docker tag $(docker images | grep mysql | tr -s " " | cut -d" " -f3) localhost:444/mysql:5.7
  sudo docker tag alpine localhost:444/alpine
  sudo docker tag $(docker images | grep prometheus | tr -s " " | cut -d" " -f3) localhost:444/prometheus


  sudo docker push localhost:444/flask-image
  sudo docker push localhost:444/emailer-image
  sudo docker push localhost:444/mysql:5.7
  sudo docker push localhost:444/alpine
  sudo docker push localhost:444/prometheus

  exit
fi

if [ "$1" == "pull" ]; then

  sudo docker image rm flask-image
  sudo docker image rm emailer-image
  sudo docker image rm $(docker images | grep mysql | tr -s " " | cut -d" " -f3)
  sudo docker image rm alpine
  sudo docker image rm $(docker images | grep prometheus | tr -s " " | cut -d" " -f3)


  sudo docker pull localhost:444/flask-image
  sudo docker pull localhost:444/emailer-image
  sudo docker pull localhost:444/mysql:5.7
  sudo docker pull localhost:444/alpine
  sudo docker pull localhost:444/prometheus

  sudo docker tag localhost:444/flask-image flask-image
  sudo docker tag localhost:444/emailer-image emailer-image
  sudo docker tag localhost:444/mysql:5.7 mysql:5.7
  sudo docker tag localhost:444/alpine alpine
  sudo docker tag localhost:444/alpine prom/prometheus

  exit
fi

if [ "$1" == "images" ]; then
  curl localhost:444/v2/_catalog

  exit
fi

if [ "$1" == "daily" ]; then
  docker exec $(docker ps | grep flask | cut -d " " -f1 | head -1) python3 dailyEmail.py

  exit
fi

if [ "$1" == "weekly" ]; then
  docker exec $(docker ps | grep flask | cut -d " " -f1 | head -1) python3 weeklyEmail.py

  exit
fi


echo Exit Docker Swarm
sudo docker swarm leave --force
sleep 1
if [ "$1" != "stop" ]; then
  echo Init Docker Swarm
  sudo docker swarm init
fi
sleep 1

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
  sudo mkdir /var/lib/car-planner/prometheus

  # copy application files
  sudo cp -R ./Flask/* /var/lib/car-planner/flask
  sudo cp -R ./MySQL/* /var/lib/car-planner/mysql-conf
  sudo cp -R ./Prometheus/* /var/lib/car-planner/prometheus

  sleep 1
fi

if [ "$1" != "stop" ] && [ "$1" != "first" ]; then
  echo "Removing /var/lib/car-planner/flask/*"
  sudo rm -rf /var/lib/car-planner/flask/*
  echo "Removing /var/lib/car-planner/mysql-conf/*"
  sudo rm -rf /var/lib/car-planner/mysql-conf/*
  echo "Removing /var/lib/car-planner/prometheus/*"
  sudo rm -rf /var/lib/car-planner/prometheus/*


  echo "Copying to /var/lib/car-planner/flask/*"
  sudo cp -R ./Flask/* /var/lib/car-planner/flask/
  echo "Copying to /var/lib/car-planner/mysql-conf/*"
  sudo cp -R ./MySQL/* /var/lib/car-planner/mysql-conf/
  echo "Copying to /var/lib/car-planner/prometheus/*"
  sudo cp -R ./Prometheus/* /var/lib/car-planner/prometheus/
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
