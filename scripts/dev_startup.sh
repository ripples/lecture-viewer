#!/usr/bin/env bash

docker-compose -f docker-compose.yml -f docker-compose-development.yml build && docker-compose -f docker-compose.yml -f docker-compose-development.yml up
