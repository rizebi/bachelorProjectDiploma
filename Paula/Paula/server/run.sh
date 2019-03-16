#!/bin/sh
docker build -t flask-image-server:latest .
docker container stop flask-container-server
docker container rm flask-container-server
docker run -d -p 5001:5000 --name flask-container-server flask-image-server
