# -*- mode: dockerfile -*-
# vi: set ft=dockerfile :

# TODO(eric.cousineau): Figure out how to make JupyterLab work with this setup:
# https://github.com/binder-examples/jupyterlab

FROM ubuntu:18.04

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
      wget \
  && rm -rf /var/lib/apt/lists/* \
  && locale-gen en_US.UTF-8

# Install later version of castxml.
# See README here: https://github.com/CastXML/CastXMLSuperbuild/tree/75ec9ef4ad48ddab605627d783bfdee57fd7bcbf
# This is v0.3.4 for Linux: https://data.kitware.com/#item/5ee7eb659014a6d84ec1f25c
RUN wget https://data.kitware.com/api/v1/file/5ee7eb659014a6d84ec1f25e/download -O /tmp/castxml.tar.gz \
  && tar xfz /tmp/castxml.tar.gz -C /usr/local --strip-components 1 \
  && rm /tmp/castxml.tar.gz

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

WORKDIR $HOME
RUN mkdir pygccxml
COPY ["/", "pygccxml/"]
RUN chown -R $NB_UID:$NB_GID \
  "$HOME/pygccxml"
USER "$NB_USER"
RUN pip3 --no-cache-dir install -e ./pygccxml[examples]
CMD ["jupyter", "lab", "--ip", "0.0.0.0", "pygccxml/docs/examples/notebook/example.ipynb"]
