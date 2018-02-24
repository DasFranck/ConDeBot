#!/bin/bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Building docker images for the $BRANCH branch"
curl -H "Content-Type: application/json" --data "{\"source_type\": \"Branch\", \"source_name\": \"$BRANCH\"}" -X POST https://registry.hub.docker.com/u/dasfranck/condebot/trigger/${DOCKER_TRIGGER_TOKEN}/