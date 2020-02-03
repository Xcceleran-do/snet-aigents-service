import sys
import grpc

sys.path.append("./service_spec")
import aigents_pb2 as pb2
import aigents_pb2_grpc as pb2_grpc


def get_news_feed(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    ch = pb2.Channel()
    ch.name = "satiretech"
    response = stub.reqJSON(ch)
    print(response)
    return response

with grpc.insecure_channel('localhost:9999') as channel:
    get_news_feed(channel)
