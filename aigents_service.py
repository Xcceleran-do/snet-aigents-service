#!/usr/bin/env python3

import sys
from concurrent import futures
import time
import grpc

from aigents import AigentsAdapter

from reputation import ReputationAdapter 

sys.path.append("./service_spec")
import aigents_pb2 as pb2
import aigents_pb2_grpc as pb2_grpc


RESP_OK = "OK"
RESP_FAIL = "FAIL"


class AigentsNewsFeed(pb2_grpc.AigentsNewsFeedServicer):
    def __init__(self):
        self.aigents = AigentsAdapter()
        self.reputation = ReputationAdapter()
     
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

    def addTopics(self, req, ctxt):
        for topic in req.topics:
            r = self.aigents.aigents_add_topic(topic.pattern)
            if r != "Ok.":
                return pb2.Response(text=RESP_FAIL)
        return pb2.Response(text=RESP_OK)

    def addSite(self, req, ctxt):
        r = self.aigents.aigents_add_site(req.url)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def addSites(self, req, ctxt):
        for site in req.sites:
            r = self.aigents.aigents_add_site(site.url)
            if r != "Ok.":
                return pb2.Response(text=RESP_FAIL)
        return pb2.Response(text=RESP_OK)

    def rmTopic(self, req, ctxt):
        r = self.aigents.aigents_remove_topic(req.pattern)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def rmTopics(self, req, ctxt):
        for topic in req.topics:
            r = self.aigents.aigents_remove_topic(topic.pattern)
            if r != "Ok.":
                return pb2.Response(text=RESP_FAIL)
        return pb2.Response(text=RESP_OK)

    def rmSite(self, req, ctxt):
        r = self.aigents.aigents_remove_site(req.url)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def rmSites(self, req, ctxt):
        for site in req.sites:
            r = self.aigents.aigents_remove_site(site.url)
            if r != "Ok.":
                return pb2.Response(text=RESP_FAIL)
        return pb2.Response(text=RESP_OK)

    def createNews(self, req, ctxt):
        r = self.aigents.aigents_create_news_item(
                req.title,
                req.date,
                req.url,
                req.img_url)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def mcreateNews(self, req, ctxt):
        for nitem in req.news_items:
            r = self.aigents.aigents_create_news_item(
                    nitem.title,
                    nitem.date,
                    nitem.url,
                    nitem.img_url)
            if r != "Ok.":
                return pb2.Response(text=RESP_FAIL)
        return pb2.Response(text=RESP_OK)

    def voteNews(self, req, ctxt):
        r = self.aigents.aigents_vote_on_item(
                req.title,
                req.date,
                req.url,
                req.vote)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def mvoteNews(self, req, ctxt):
        for nitem in req.news_items:
            r = self.aigents.aigents_vote_on_item(
                    nitem.title,
                    nitem.date,
                    nitem.url,
                    nitem.vote)
            if r != "Ok.":
                return pb2.Response(text=RESP_FAIL)
        return pb2.Response(text=RESP_OK)

    def rmNews(self, req, ctxt):
        r = self.aigents.aigents_rm_news_item(
                req.title,
                req.date,
                req.url)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def mrmNews(self, req, ctxt):
        for nitem in req.news_items:
            r = self.aigents.aigents_rm_news_item(
                    nitem.title,
                    nitem.date,
                    nitem.url)
            if r != "Ok.":
                return pb2.Response(text=RESP_FAIL)
        return pb2.Response(text=RESP_OK)

    def mkFriend(self, req, ctxt):
        r = self.aigents.aigents_friend(req.email, req.action)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def mkFriends(self, req, ctxt):
        for paction in req.peer_actions:
            r = self.aigents.aigents_friend(paction.email, paction.action)
            if r != "Ok.":
                return pb2.Response(text=RESP_FAIL)
        return pb2.Response(text=RESP_OK)

    def sharePeer(self, req, ctxt):
        r = self.aigents.aigents_peer_share(req.email, req.action)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def sharePeers(self, req, ctxt):
        for paction in req.peer_actions:
            r = self.aigents.aigents_peer_share(paction.email, paction.action)
            if r != "Ok.":
                return pb2.Response(text=RESP_FAIL)
        return pb2.Response(text=RESP_OK)

    def receivePeer(self, req, ctxt):
        r = self.aigents.aigents_peer_receive(req.email, req.action)
        if r == "Ok.":
            return pb2.Response(text=RESP_OK)
        return pb2.Response(text=RESP_FAIL)

    def receivePeers(self, req, ctxt):
        for paction in req.peer_actions:
            r = self.aigents.aigents_peer_receive(paction.email, paction.action)
            if r != "Ok.":
                return pb2.Response(text=RESP_FAIL)
        return pb2.Response(text=RESP_OK)

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

    # Reputation System Grpc service
    def createSession(self, req, ctxt):
        r = self.reputation.create_session()
        return pb2.Response(text=r)
        
    def closeSession(self, req, ctxt):
        r = self.reputation.close_session()
        return pb2.Response(text=r)
        
    def req(self, req, ctxt):
        r = self.reputation.request(req.text)
        return pb2.Response(text=r)
        
    def reputationRequest(self, req, ctxt):
        r = self.reputation.reputation_request(req.text)
        return pb2.Response(text=r)
    
    def setParameters(self, req, ctxt):
        param = {'default' : req.default, 'decayed' : req.decayed, 'conservatism' : req.conservatism, 'precision' : req.precision, 
                 'update_period' : req.update_period, 'aggregation' : req.aggregation, 'downrating' : req.downrating, 
                 'ratings' : req.ratings, 'spendings' : req.spendings, 'parents' : req.parents, 'predictiveness' : req.predictiveness}
        r = self.reputation.set_parameters(param)
        return pb2.Response(text=r)
        
    def getParameters(self, req, ctxt):
        r = self.reputation.get_parameters()
        return pb2.Param(default = r['default'], decayed = r['decayed'], conservatism = r['conservatism'], precision = r['precision'],
                       liquid = r['liquid'], update_period = r['update_period'], aggregation = r['aggregation'], downrating = r['downrating'], 
                       fullnorm = r['fullnorm'], weighting = r['weighting'], denomination = r['denomination'], 
                       logratings = r['logratings'], ratings = r['ratings'], spendings = r['spendings'], parents = r['parents'], 
                       predictiveness = r['predictiveness'], rating_bias = r['rating_bias'], unrated = r['unrated'])

    def setParent(self, req, ctxt): #parent_id, list_of_children_ids
        r = self.reputation.set_parent(req.parent_id, req.child_id)
        return pb2.Response(text=r)
        
    def putRanks(self, req, ctxt): #date, ranks):
        arr = []
        ls = list(req.rank_val)
        length = len(ls) 
        for i in range(length):
            arr.append({'id':ls[i].id,'rank':ls[i].rank})        
        r = self.reputation.put_ranks(req.date, arr)
        return pb2.Response(text=r)
    
    def getRanks(self, req, ctxt):
        filter = {"ids ": req.ids, "date" : req.date}
        ls = self.reputation.get_ranks(filter)
        r = " ".join(str(x) for x in ls)
        return pb2.Response(text=r)
    
    def updateRanks(self, req, ctxt):
        r = self.reputation.update_ranks(req.date)    
        return pb2.Response(text=r)
        
    def clearRanks(self, req, ctxt):
        r = self.reputation.clear_ranks()
        return pb2.Response(text=r)
            
    def putRatings(self, req, ctxt):
        arr = []
        rat_arr = list(req.rating_val)
        length = len(rat_arr) 
        for i in range(length):
            arr.append({'from': rat_arr[i].from_rate,'type': rat_arr[i].type_rate, 'to': rat_arr[i].to_rate,'value': rat_arr[i].value,
                        'weight': rat_arr[i].weight,'time': rat_arr[i].time})        
        r = self.reputation.put_ratings(arr)
        return pb2.Response(text=r)
            
    def getRatings(self, req, ctxt):
        filter = {"ids": " " + req.ids, "since" : req.since, "until": req.until}
        ls = self.reputation.get_ratings(filter)
        r = " ".join(str(x) for x in ls)
        return pb2.Response(text=r)
                
    def clearRatings(self, req, ctxt):
        r = self.reputation.clear_ratings()
        return pb2.Response(text=r)

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
