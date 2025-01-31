# -*- mode: dockerfile -*-
# vi: set ft=dockerfile :

# TODO(eric.cousineau): Figure out how to make JupyterLab work with this setup:
# https://github.com/binder-examples/jupyterlab

# TODO(eric.cousineau): See if it's easier to use a conda-based workflow, or a
# simpler Docker base image, to use Eigen headers, rather than doing a custom
# Docker image:
# https://mybinder.readthedocs.io/en/latest/using/config_files.html

FROM ubuntu:22.04

ARG NB_USER=jovyan
ARG NB_UID=1000
ARG NB_GID=100
EXPOSE 7000/tcp
EXPOSE 8888/tcp

RUN export DEBIAN_FRONTEND=noninteractive \
  && apt-get update \
  && apt-get install -y --no-install-recommends \
    -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confnew \
    -o Dpkg::Use-Pty=0 \
      locales \
      python3-pip \
      python3-setuptools \
  && rm -rf /var/lib/apt/lists/* \
  && locale-gen en_US.UTF-8

# Install common C++ libraries for experimenting. These are not necessary to
# use pygccxml itself.
RUN export DEBIAN_FRONTEND=noninteractive \
  && apt-get update \
  && apt-get install -y --no-install-recommends \
    -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confnew \
    -o Dpkg::Use-Pty=0 \
      libeigen3-dev \
      libstdc++-7-dev \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -d "/home/$NB_USER" -G $NB_GID -mU -s /bin/bash "$NB_USER"
ENV HOME="/home/$NB_USER" \
  LANG=en_US.UTF-8 \
  LANGUAGE=en_US.UTF-8 \
  LC_ALL=en_US.UTF-8 \
  SHELL=/bin/bash \
  USER="$NB_USER" \
  PATH="/home/$NB_USER/.local/bin:/usr/local/bin:/usr/bin:/bin"

# Upgrade pip to use newer indices for castxml.
# WARNING: Never upgrade a distribution `pip` on a host system using sudo!
# We are only doing this for a transient Docker image. For a host system, use a
# virtualenv to upgrade pip.
RUN pip3 --no-cache-dir install -U pip

WORKDIR $HOME
RUN mkdir pygccxml
COPY ["/", "pygccxml/"]
RUN chown -R $NB_UID:$NB_GID \
  "$HOME/pygccxml"
USER "$NB_USER"
RUN pip3 --no-cache-dir install castxml
RUN pip3 --no-cache-dir install -e ./pygccxml[examples]
CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "pygccxml/docs/examples/notebook/example.ipynb"]
