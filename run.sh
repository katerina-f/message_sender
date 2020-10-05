#!/bin/bash

docker volume create --name=redis
docker volume create --name=app_container
docker volume create --name=worker_container

docker-compose up -d --build
