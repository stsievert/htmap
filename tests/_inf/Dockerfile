# Copyright 2019 HTCondor Team, Computer Sciences Department,
# University of Wisconsin-Madison, WI.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# this dockerfile builds a test environment for HTMap

FROM ubuntu:bionic

# switch to root to do root-level config
USER root

# build config
ARG PYTHON_VERSION=3.7
ARG HTCONDOR_VERSION=8.8
ARG MINICONDA_VERSION=latest

# environment setup
ENV DEBIAN_FRONTEND=noninteractive
#    LC_ALL=en_US.UTF-8 \
#    LANG=en_US.UTF-8 \
#    LANGUAGE=en_US.UTF-8

# faster container builds
RUN apt-get update \
 && apt-get -y install --no-install-recommends software-properties-common \
 && add-apt-repository ppa:apt-fast/stable \
 && apt-get update \
 && apt-get -y install apt-fast \
 && apt-get -y clean \
 && rm -rf /var/lib/apt/lists/*

# install utils and dependencies
RUN apt-fast update \
 && apt-fast -y install --no-install-recommends sudo vim less build-essential git gnupg wget ca-certificates locales python3 python3-pip python3-setuptools \
 && apt-get -y clean \
 && rm -rf /var/lib/apt/lists/*
# && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
# && locale-gen

# install HTCondor version specified in config
RUN wget -qO - https://research.cs.wisc.edu/htcondor/ubuntu/HTCondor-Release.gpg.key | apt-key add - \
 && echo "deb http://research.cs.wisc.edu/htcondor/ubuntu/${HTCONDOR_VERSION}/bionic bionic contrib" >> /etc/apt/sources.list \
 && apt-fast -y update \
 && apt-fast -y install --no-install-recommends htcondor \
 && apt-get -y clean \
 && rm -rf /var/lib/apt/lists/*

# create a user to be our submitter and set conda install location
ENV SUBMIT_USER=mapper
RUN groupadd ${SUBMIT_USER} \
 && useradd -m -g ${SUBMIT_USER} ${SUBMIT_USER}

# switch to submit user, don't need root anymore
USER ${SUBMIT_USER}

# install htmap dependencies early for docker build caching
COPY requirements.txt /home/${SUBMIT_USER}/requirements.txt
COPY requirements-dev.txt /home/${SUBMIT_USER}/requirements-dev.txt
RUN pip3 install --no-cache -r /home/${SUBMIT_USER}/requirements-dev.txt \
 && rm /home/${SUBMIT_USER}/requirements*

# set default entrypoint and command
# the entrypoint is critical: it starts HTCondor in the container
ENTRYPOINT ["tests/_inf/entrypoint.sh"]
CMD ["pytest"]

# copy HTCondor and HTMap testing configs into place
COPY tests/_inf/condor_config.local /etc/condor/condor_config.local
COPY tests/_inf/.htmaprc /home/${SUBMIT_USER}/.htmaprc

# copy htmap package into container and install it
# this is the only part that can't be cached against editing the package
COPY --chown=mapper:mapper . /home/${SUBMIT_USER}/htmap
WORKDIR /home/${SUBMIT_USER}/htmap
RUN chmod +x /home/${SUBMIT_USER}/htmap/tests/_inf/entrypoint.sh /home/${SUBMIT_USER}/htmap/tests/_inf/travis.sh \
 && pip3 install --no-cache --no-deps -e .
