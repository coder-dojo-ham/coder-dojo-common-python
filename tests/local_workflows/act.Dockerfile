
FROM python:3.11.2-slim as base

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends curl git unzip patch && \
    apt-get clean autoclean && \
    apt-get autoremove --yes && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/lib/{apt,dpkg,cache,log}

RUN mkdir -p "/github/workspace"

#####################
# Install Act #
#####################
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl https://raw.githubusercontent.com/nektos/act/master/install.sh | bash

WORKDIR /github/workspace
