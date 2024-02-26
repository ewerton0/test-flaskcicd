#!/bin/bash

echo "This Script is used to stop already running docker container, remove them and remove the image as well"

sudo docker stop $(docker ps -a -q)

sudo docker rm $(sudo docker ps -a -q)

sudo docker rmi $(sudo docker images -q)