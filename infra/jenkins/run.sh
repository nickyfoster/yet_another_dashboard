#!/bin/bash

docker-compose -f docker-compose.yml kill
docker-compose -f docker-compose.yml rm -f
docker-compose -f docker-compose.yml pull
docker-compose -f docker-compose.yml up -d