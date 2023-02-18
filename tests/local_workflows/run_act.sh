#!/bin/bash

set -eu

docker build . -f act.Dockerfile -t coderdojo_act
docker build . -f runner.Dockerfile -t coderdojo_act_runner:20.04
# set event to push
EVENT=push
# JOB
JOB_NAME=${1:-lint}

# Prepare the act command
ACT_CMD="act \
    --eventpath tests/local_workflows/${EVENT}.json \
    -P ubuntu-latest=coderdojo_act_runner:20.04 \
    --pull=false \
    -j ${JOB_NAME} \
    ${EVENT} \
"

docker run --rm -v "$(pwd)/../..:/github/workspace" -v /var/run/docker.sock:/var/run/docker.sock coderdojo_act ${ACT_CMD}
