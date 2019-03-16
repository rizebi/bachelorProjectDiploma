#!/bin/sh
docker build -t image-server:latest .
docker stop container-server
docker rm container-server
docker run -d -p 8001:5000 --name container-server image-server
