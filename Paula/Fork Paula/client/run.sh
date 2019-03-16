#!/bin/sh
docker build -t image-client:latest .
docker stop container-client
docker rm container-client
docker run -d -p 8000:5000 --name container-client image-client
