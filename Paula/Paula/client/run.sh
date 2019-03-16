#!/bin/sh
docker build -t flask-image:latest .
docker container stop flask-container
docker container rm flask-container
docker run -d -p 5000:5000 --name flask-container flask-image
