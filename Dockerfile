# Dockerfile for Aigents SNET Service (Server)

FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y \
        apt-utils \
        curl \
        wget \
        vim \
        git \
        zip \
        libudev-dev \
        libusb-1.0.0-dev \
        python3 \
        python3-pip

RUN pip3 install snet-cli

RUN cd /tmp && \
    wget "https://github.com/singnet/snet-daemon/releases/download/v3.1.1/snet-daemon-v3.1.1-linux-amd64.tar.gz" && \
    tar -xvf snet-daemon-v3.1.1-linux-amd64.tar.gz && \
    mv snet-daemon-v3.1.1-linux-amd64/snetd /usr/local/bin/snetd

# install grpc
RUN apt-get install -y build-essential \
        autoconf \
        libtool \
        pkg-config \
        libgflags-dev \
        libgtest-dev \
        clang \
        libc++-dev && \
    cd tmp && \
    git clone -b $(curl -L https://grpc.io/release) https://github.com/grpc/grpc && \
    cd grpc && \
    git submodule update --init && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd third_party/protobuf && \
    make install && \
    ldconfig

# set working dir
WORKDIR /singnet/aigents
ADD . /singnet/aigents

RUN protoc --proto_path=service_spec \
           --python_out=service_spec \
           --grpc_out=service_spec \
           --plugin=protoc-gen-grpc=$(which grpc_python_plugin) \
           ./service_spec/aigents.proto

RUN protoc --proto_path=service_spec \
           --php_out=service_spec \
           --grpc_out=service_spec \
           --plugin=protoc-gen-grpc=$(which grpc_php_plugin) \
           ./service_spec/aigents.proto
