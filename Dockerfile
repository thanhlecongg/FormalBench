FROM ubuntu:20.04

RUN set -ex && \
    apt-get update && \
    apt-get install -y \
        curl

RUN set -ex && \
    curl \
        -1sLf 'https://dl.cloudsmith.io/public/mull-project/mull-stable/setup.deb.sh' | bash

RUN set -ex && \
    apt-get update && \
    apt-get install -y \
        mull-12

RUN set -ex && \
    apt-get install -y \
        clang-12