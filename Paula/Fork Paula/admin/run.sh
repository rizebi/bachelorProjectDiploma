#!/bin/sh
docker build -t image-admin:latest .
docker stop container-admin
docker rm container-admin
docker run -d -p 8002:5000 --name container-admin image-admin
