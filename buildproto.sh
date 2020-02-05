#!/bin/bash
/usr/local/bin/protoc --proto_path=service_spec --php_out=service_spec --grpc_out=service_spec --plugin=protoc-gen-grpc=/usr/bin/grpc_php_plugin ./service_spec/aigents.proto
/usr/local/bin/protoc --proto_path=service_spec --python_out=service_spec --grpc_out=service_spec --plugin=protoc-gen-grpc=/usr/bin/grpc_python_plugin service_spec/aigents.proto
#python3 -m grpc_tools.protoc -I./service_spec --python_out=./service_spec --grpc_python_out=./service_spec ./service_spec/aigents.proto
