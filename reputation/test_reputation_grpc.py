import sys
import grpc

sys.path.append("./service_spec")
import service_spec.reputation_pb2 as pb2
import service_spec.reputation_pb2_grpc as pb2_grpc
from reputation import settings
from datetime import datetime, date

def create_session(channel):
    stub = pb2_grpc.ReputationFeedStub(channel)
    r = pb2.Input(text=" ")
    resp = stub.createSession(r)
    print("Called Create Session --->", resp)
    assert resp.text.upper() == "OK"

def close_session(channel):
    stub = pb2_grpc.ReputationFeedStub(channel)
    r = pb2.Input(text=" ")
    resp = stub.closeSession(r)
    print("Called Close Session --->", resp)
    assert resp.text.upper() == "OK."
    
def req(channel):
    stub = pb2_grpc.ReputationFeedStub(channel)
    r = pb2.Input(text="what my email.")
    resp = stub.req(r)
    print("Called Request --->", resp.text)
    assert "Your email" in resp.text

def reputation_request(channel):
    stub = pb2_grpc.ReputationFeedStub(channel)
    setting = settings.ReputationSettings()
    r = pb2.Input(text=setting.AIGENTS_LOGIN_NAME + " " + "set parent 5 child 4")
    resp = stub.reputationRequest(r)
    print("Called Reputation Request --->", resp)
    assert "OK" in resp.text.upper()

def set_parameters(channel):
    stub = pb2_grpc.ReputationFeedStub(channel)
    r = pb2.Param(default = 0.0, decayed = 0.5, conservatism = 0.5, precision = 1, update_period = 1, aggregation = False, downrating = False,
                  ratings = 1.0, spendings = 0.0, parents = "0.0", predictiveness = "0.0")
    resp = stub.setParameters(r)
    print("Called Set Parameters --->", resp)
    assert "OK" in resp.text.upper()

def get_parameters(channel):
    stub = pb2_grpc.ReputationFeedStub(channel)
    r = pb2.Input(text=" ")
    resp = stub.getParameters(r)
    print("Called Get Parameters --->", resp.default)
    assert resp.default == 0.0

def set_parent(channel):
    stub = pb2_grpc.ReputationFeedStub(channel)
    r = pb2.Parent(parent_id = "6", child_id = "[7 9]")
    resp = stub.setParent(r)
    print("Called Set Parent --->", resp)
    assert resp.text == "OK"

# you can't put two ranks in same date value for a certain ID
def put_ranks(channel):
    stub = pb2_grpc.ReputationFeedStub(channel)
    r = pb2.Ranks(
        date = str(date(2011, 6, 2)),
        rank_val=[
            pb2.Rank(id=901, rank=78),
            pb2.Rank(id=821, rank=13)
        ]
    )
    resp = stub.putRanks(r)
    print("Called Put Ranks --->", resp)
    assert resp.text == "OK"
    
# needs to set id and date to exisitng record
def get_ranks(channel):
    stub = pb2_grpc.ReputationFeedStub(channel)
    r = pb2.RankRequest(date=str(date(2011, 6, 2)), ids = "991")
    resp = stub.getRanks(r)
    print("Called Get Ranks --->", resp)
    assert "id" in resp.text
    
# you can not update ranks with a similar date twice
def update_ranks(channel):
    stub = pb2_grpc.ReputationFeedStub(channel)
    r = pb2.RankUpdate(date=str(date(2002, 12, 11)))
    resp = stub.updateRanks(r)
    print("Called Update Ranks --->", resp)
    assert "OK" in resp.text.upper()

# would erase all ranking records
def clear_ranks(channel):
    stub = pb2_grpc.ReputationFeedStub(channel)
    r = pb2.Input(text=" ")
    resp = stub.clearRanks(r)
    print("Called Clear Ranks --->", resp)
    assert "OK" in resp.text.upper()

# you can't put two ratings in same date value for a certain ID    
def put_ratings(channel):
    stub = pb2_grpc.ReputationFeedStub(channel)
    r = pb2.Ratings(
        rating_val=[
            pb2.Rating(from_rate='425', type_rate='rating', to_rate='366', value=6, weight=4, time=str(date(2000, 1, 6))),
            pb2.Rating(from_rate='122', type_rate='rating', to_rate='652', value=8, weight=5, time=str(date(2014, 2, 11)))
        ]
    )
    resp = stub.putRatings(r)
    print("Called Put Ratings --->", resp)
    assert resp.text == "OK"
    
# needs to set id and date to exisitng record
def get_ratings(channel):
    stub = pb2_grpc.ReputationFeedStub(channel)
    r = pb2.RatingFilter(ids='425', since =str(date(2003, 11, 11)), until=str(date(2020, 11, 11)))
    resp = stub.getRatings(r)
    print("Called Get Ratings --->", resp)
    assert "type" in resp.text

# would erase all rating records
def clear_ratings(channel):
    stub = pb2_grpc.ReputationFeedStub(channel)
    r = pb2.Input(text=" ")
    resp = stub.clearRatings(r)
    print("Called Clear Ratings --->", resp)
    assert "OK" in resp.text.upper()    
    
with grpc.insecure_channel('localhost:9998') as channel:
    create_session(channel)
    req(channel)
    reputation_request(channel)
    set_parameters(channel)
    get_parameters(channel)
    set_parent(channel)
    put_ranks(channel)
    get_ranks(channel)
    update_ranks(channel)
    put_ratings(channel)
    get_ratings(channel)
    clear_ranks(channel)
    clear_ratings(channel)
    close_session(channel)   