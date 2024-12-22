FROM python:3.10

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on

RUN apt update && \
    apt -y upgrade && \
    apt install -y --no-install-recommends \
        software-properties-common \
        build-essential \
        python3-pip \
        python3-tk \
        python3-dev \
        git \
        bash \
        libsm6 \
        libgl1 \
        libxrender1 \
        libxext6 \
        wget \
        curl \
        zip \
        unzip \
        libtcmalloc-minimal4 \
        ca-certificates && \
    update-ca-certificates && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen

WORKDIR /embedder

COPY requirements.txt /embedder/
RUN pip install -r requirements.txt --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cu121
RUN pip install datasets einops