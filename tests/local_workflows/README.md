# Local Workflows

Tools to test a workflow locally.

This will allow you to test a workflow locally, without having to push to a branch or open a PR yet.

## Requirements

- [Docker](https://docs.docker.com/get-docker/)
- Bash

## Usage

1. Clone the repository
2. cd into tests/local_workflows
3. Use `run_act.sh [job_name]` to run a workflow job locally.

## Issues

The `act` tool has some issues.

- Python setup will show a post action error around caching, but the job will still run.
- Caches are fake, it will not actually cache anything.

## Maintaining

Act has images that emulate github runners, however the default choices are minimal a nd medium without python, or full which is 20Gb.

The runner.Dockerfile has is based on a medium image, but with python installed. This is the image that is used for the local workflow. If tools expected in github runners are missing, they can be added to this Dockerfile.
The script `run_act.sh` will build the image if it does not exist.
