import sys
import grpc

sys.path.append("./service_spec")
import aigents_pb2 as pb2
import aigents_pb2_grpc as pb2_grpc

def user_signup(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    ui = pb2.UserInfo()
    ui.name = "TestName"
    ui.surname = "TestSurname"
    ui.email = "test@testemail.io"
    ui.secret_question = "testQuestion"
    ui.secret_answer = "testAnswer"
    resp = stub.userSignup(ui)
    print("Called userSignup ---> ", resp)
    assert resp.text == "OK"

def user_login(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    ui = pb2.UserInfo()
    ui.email = "test@testemail.io"
    ui.secret_question = "testQuestion"
    ui.secret_answer = "testAnswer"
    resp = stub.userLogin(ui)
    print("Called userLogin ---> ", resp)
    assert resp.text == "OK"

def add_topic(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    t = pb2.Topic()
    t.pattern = '{test pattern [for topic]}'
    resp = stub.addTopic(t)
    print("Called addTopic ---->" , resp)
    assert resp.text == "OK"

def add_site(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    s = pb2.Site()
    s.url = 'https://test-url.io'
    resp = stub.addSite(s)
    print("Called addSite --->" , resp)
    assert resp.text == "OK"

def remove_topic(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    t = pb2.Topic()
    t.pattern = '{non existant test pattern [for topic]}'
    resp = stub.rmTopic(t)
    print("Called rmTopic to fail ---->" , resp)
    assert resp.text == "FAIL"
    t = pb2.Topic()
    t.pattern = '{test pattern [for topic]}'
    resp = stub.rmTopic(t)
    print("Called rmTopic ---->" , resp)
    assert resp.text == "OK"

def remove_site(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    s = pb2.Site()
    s.url = 'https://test-url.io'
    resp = stub.rmSite(s)
    print("Called rmSite ---->" , resp)
    assert resp.text == "OK"

def create_news(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    ni = pb2.NewsItem()
    ni.title = "Test Article Title"
    ni.date = "2020-01-30"
    ni.url = "https://aigents.icog-labs.com"
    resp = stub.createNews(ni)
    print("Called createNews ---->" , resp)
    assert resp.text == "OK"

def vote_news(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    ni = pb2.NewsItem()
    ni.title = "Test Article Title"
    ni.date = "2020-01-30"
    ni.url = "https://aigents.icog-labs.com"
    ni.vote = 0
    resp = stub.voteNews(ni)
    print("Called voteNews ---->" , resp)
    assert resp.text == "OK"

def remove_news(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    ni = pb2.NewsItem()
    ni.title = "Test Article Title"
    ni.date = "2020-01-30"
    ni.url = "https://aigents.icog-labs.com"
    resp = stub.rmNews(ni)
    print("Called rmNews ---->" , resp)
    assert resp.text == "OK"

def get_news_feed(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    ch = pb2.Channel()
    ch.name = "satiretech"
    response = stub.reqJSON(ch)
    print(response)
    return response

with grpc.insecure_channel('localhost:9999') as channel:
    user_signup(channel)
    user_login(channel)
    add_topic(channel)
    add_site(channel)
    remove_topic(channel)
    remove_site(channel)
    get_news_feed(channel)
