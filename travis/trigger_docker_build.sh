#!/bin/bash
if [ "$BRANCH" = "dev" ] || [ "$BRANCH" = "master" ]; then 
    curl -H "Content-Type: application/json" --data '{"source_type": "Branch", "source_name": "$BRANCH"}' -X POST https://registry.hub.docker.com/u/dasfranck/condebot/trigger/${DOCKER_TRIGGER_TOKEN}/
fi