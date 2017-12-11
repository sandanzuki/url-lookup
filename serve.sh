#! /bin/bash

docker build -t service service
docker build -t redis redis

docker run --net=host --publish 5000:5000 --name service --rm service &
docker run --net=host --publish 6379:6379 --name redis -d redis &
