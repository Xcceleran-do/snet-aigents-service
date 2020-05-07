# Reputation Service 

This repository contains early pre-alpha proof-of-concept developments and experiments for Reputation system of SingularityNET.

Main project page: https://github.com/singnet/reputation

Here the Reputation Service API is used to integrate it with snet-aigents-service and eventually have a grpc endpoint and singularitynet daemon configuration

# Testing

Point to a running aigents instance in settings.py (needs to be an admin account)

python3 aigents_reputation_service.py # for python module

python3 -m grpc_tools.protoc -I service_spec --python_out=service_spec/ --grpc_python_out=service_spec/ service_spec/reputation.proto

python3 test_reputation_grpc.py # for grpc endpoint