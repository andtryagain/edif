#!/bin/bash

docker image build -t flask_docker .
# docker image build -t flask_docker . --build-arg INTERNAL_PORT=3000 EXTERNAL_PORT=3000

docker run -p 3000:3000 -d flask_docker
