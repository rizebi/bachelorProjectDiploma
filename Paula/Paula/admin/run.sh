#!/bin/sh
docker build -t flask-image-admin:latest .
docker container stop flask-container-admin
docker container rm flask-container-admin
docker run -d -p 5002:5000 --name flask-container-admin flask-image-admin
