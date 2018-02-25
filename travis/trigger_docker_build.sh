#!/bin/bash
echo "Triggering a docker image build for the $TRAVIS_BRANCH branch"
curl -H "Content-Type: application/json" --data "{\"source_type\": \"Branch\", \"source_name\": \"$TRAVIS_BRANCH\"}" -X POST https://registry.hub.docker.com/u/dasfranck/condebot/trigger/${DOCKER_TRIGGER_TOKEN}/