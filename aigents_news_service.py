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
REDP_FAIL = "FAIL"


class AigentsNewsFeed(pb2_grpc.AigentsNewsFeedServicer):
    def __init__(self):
        self.aigents = AigentsAdapter()
    
    def userLogin(self, req, ctxt):
        user_email = req.email;
        user_sec_q = req.secret_question;
        user_sec_a = req.secret_answer;

        self.aigents.aigents_login(user_email, user_sec_q, user_sec_a);
        r = self.aigents.aigents_getemail()
        
        #TODO better success/fail check
        if r[0]["email"] == user_email:
            return RESP_OK
        return RESP_FAIL

    def addTopic(self, req, ctxt):
        r = self.aigents.aigents_set_topics(req.label, req.pattern)
        if r.text == "Ok.":
            return RESP_OK
        return RESP_FAIL

    def addSites(self, req, ctxt):
        r = self.aigents.aigents_set_sites(req.site)

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
        print("-------------------------")
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
