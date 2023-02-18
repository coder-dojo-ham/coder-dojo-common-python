## This creates a python environment on top of the act medium image
FROM catthehacker/ubuntu:act-20.04
## Setup python packages
RUN apt-get -yq update && apt-get -yq install --no-install-recommends \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

## Setup pipx (see https://github.com/actions/runner-images/blob/ubuntu22/20230109.1/images/linux/scripts/installers/python.sh)
ENV PIPX_BIN_DIR=/opt/pipx_bin
ENV PIPX_HOME=/opt/pipx

RUN python3 -m pip install --no-cache-dir pipx && \
    python3 -m pipx ensurepath

ENV PATH="${PIPX_BIN_DIR}:${PATH}"
