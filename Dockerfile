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
RUN apt-get update
RUN pip3 install snet-cli

RUN cd /tmp && \
    wget "https://github.com/singnet/snet-daemon/releases/download/v4.0.0/snet-daemon-v4.0.0-linux-amd64.tar.gz" && \
    tar -xvf snet-daemon-v4.0.0-linux-amd64.tar.gz && \
    mv snet-daemon-v4.0.0-linux-amd64/snetd /usr/local/bin/snetd

RUN apt-get update

RUN apt-get install cmake -y 
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
    make grpc_php_plugin    

RUN  cd tmp/grpc && \
    make -j$(nproc) && \
    ldconfig

RUN  cd tmp/grpc && \
    cd third_party/protobuf && \
    make install && \
    ldconfig

RUN pip3 install --upgrade protobuf

# set working dir
WORKDIR /singnet/aigents
ADD . /singnet/aigents

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

ENV LANG en_US.UTF-8


RUN python3 -m grpc_tools.protoc --proto_path=service_spec --python_out=service_spec --grpc_python_out=service_spec ./service_spec/aigents.proto

RUN protoc --proto_path=service_spec \
           --php_out=service_spec \
           --grpc_out=service_spec \
           --plugin=protoc-gen-grpc=/tmp/grpc/bins/opt/grpc_php_plugin \
           ./service_spec/aigents.proto

RUN pip3 install supervisor
RUN mkdir -p /var/log/supervisor
