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

def add_topics(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    t0 = pb2.Topic(pattern='{test pattern one [for topic one]}')
    t1 = pb2.Topic(pattern='{test pattern two [for topic two]}')
    ts = pb2.Topics()
    ts.topics.extend([t0, t1])
    resp = stub.addTopics(ts)
    print("Called addTopics ---->" , resp)
    assert resp.text == "OK"

def add_site(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    s = pb2.Site()
    s.url = 'https://test-url.io'
    resp = stub.addSite(s)
    print("Called addSite --->" , resp)
    assert resp.text == "OK"

def add_sites(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    s0 = pb2.Site(url="http://test-url-one.com")
    s1 = pb2.Site(url="http://test-url-two.com")
    ss = pb2.Sites()
    ss.sites.extend([s0, s1])
    resp = stub.addSites(ss)
    print("Called addSites --->" , resp)
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

def remove_topics(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    t0 = pb2.Topic(pattern='{test pattern one [for topic one]}')
    t1 = pb2.Topic(pattern='{test pattern two [for topic two]}')
    ts = pb2.Topics()
    ts.topics.extend([t0, t1])
    resp = stub.rmTopics(ts)
    print("Called rmTopics ---->" , resp)
    assert resp.text == "OK"

def remove_site(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    s = pb2.Site()
    s.url = 'https://test-url.io'
    resp = stub.rmSite(s)
    print("Called rmSite ---->" , resp)
    assert resp.text == "OK"

def remove_sites(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    s0 = pb2.Site(url="http://test-url-one.com")
    s1 = pb2.Site(url="http://test-url-two.com")
    ss = pb2.Sites()
    ss.sites.extend([s0, s1])
    resp = stub.rmSites(ss)
    print("Called rmSites --->" , resp)
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

def make_friend(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    pa = pb2.PeerAction()
    pa.email = "dagim@icog-labs.com"
    pa.action = True
    resp = stub.mkFriend(pa)
    print("Called mkFriend ---->" , resp)
    assert resp.text == "OK"

def share_to_peer(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    pa = pb2.PeerAction()
    pa.email = "dagim@icog-labs.com"
    pa.action = True
    resp = stub.sharePeer(pa)
    print("Called sharePeer ---->" , resp)
    assert resp.text == "OK"

def receive_from_peer(channel):
    stub = pb2_grpc.AigentsNewsFeedStub(channel)
    pa = pb2.PeerAction()
    pa.email = "dagim@icog-labs.com"
    pa.action = True
    resp = stub.receivePeer(pa)
    print("Called receivePeer ---->" , resp)
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
    add_topics(channel)
    add_site(channel)
    add_sites(channel)
    remove_topic(channel)
    remove_topics(channel)
    remove_site(channel)
    remove_sites(channel)
    make_friend(channel)
    share_to_peer(channel)
    receive_from_peer(channel)
    get_news_feed(channel)
