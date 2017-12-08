#! /bin/bash

docker build . -t service
docker run --net=host --publish 5000:5000 --name service --rm service &
