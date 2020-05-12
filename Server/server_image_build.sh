#!/usr/bin/env bash
docker container stop simple_vote
docker container rm simple_vote
docker image rm simple_vote:0.0.1
docker image build -t simple_vote:0.0.1 .
docker container run --name=simple_vote -v $(pwd)/server_log:/usr/src/app/log -d -p 8700:8201 -it simple_vote:0.0.1
