#!/usr/bin/env python3

import sys
from concurrent import futures
import time
import grpc

from aigents import AigentsAdapter

sys.path.append("./service_spec")
import aigents_pb2 as pb2
import aigents_pb2_grpc as pb2_grpc


RESP_OK = "OK"
RESP_FAIL = "FAIL"


class AigentsNewsFeed(pb2_grpc.AigentsNewsFeedServicer):
    def __init__(self):
        self.aigents = AigentsAdapter()
    
    def userSignup(self, req, ctxt):
        user_f_name = req.name
        user_l_name = req.surname
        user_email = req.email
        user_sec_q = req.secret_question
        user_sec_a = req.secret_answer
        self.aigents.aigents_signup(user_f_name, user_l_name,
                                    user_email, user_sec_q,
                                    user_sec_a);
        #TODO better success/fail check
        r = self.aigents.aigents_get_email()
        if r == user_email:
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def userLogin(self, req, ctxt):
        user_email = req.email
        user_sec_q = req.secret_question
        user_sec_a = req.secret_answer
        self.aigents.aigents_login(user_email, user_sec_q, user_sec_a);
        #TODO better success/fail check
        r = self.aigents.aigents_get_email()
        if r == user_email:
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def addTopic(self, req, ctxt):
        r = self.aigents.aigents_add_topic(req.pattern)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def addSite(self, req, ctxt):
        r = self.aigents.aigents_add_site(req.url)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def rmTopic(self, req, ctxt):
        r = self.aigents.aigents_remove_topic(req.pattern)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def rmSite(self, req, ctxt):
        r = self.aigents.aigents_remove_site(req.url)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def createNews(self, req, ctxt):
        r = self.aigents.aigents_create_news_item(
                req.title,
                req.date,
                req.url,
                req.img_url)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def voteNews(self, req, ctxt):
        r = self.aigents.aigents_vote_on_item(
                req.title,
                req.date,
                req.url,
                req.vote)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def rmNews(self, req, ctxt):
        r = self.aigents.aigents_rm_news_item(
                req.title,
                req.date,
                req.url)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def mkFriend(self, req, ctxt):
        r = self.aigents.aigents_friend(req.email, req.action)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def sharePeer(self, req, ctxt):
        r = self.aigents.aigents_peer_share(req.email, req.action)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def receivePeer(self, req, ctxt):
        r = self.aigents.aigents_peer_receive(req.email, req.action)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def reqRSS(self, req, ctxt):
        response = pb2.Feeds()
        resp = self.aigents.aigents_get_rss(req.name)
        for r in resp:
            feed = self.response.news_feed.add()
            feed.title = r["title"]
            feed.link = r["link"]
            feed.description = r["description"]
            feed.img_url = ""
        return response
    
    def reqJSON(self, req, ctxt):
        r = pb2.Response()
        r.text = self.aigents.aigents_get_news(req.name)
        return r


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_AigentsNewsFeedServicer_to_server(AigentsNewsFeed(), server)
    server.add_insecure_port('[::]:9999')
    server.start()
    print("Server listening on 0.0.0.0:{}".format(9999))
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    main()
