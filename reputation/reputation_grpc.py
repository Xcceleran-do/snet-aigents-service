#!/usr/bin/env python3

import sys
from concurrent import futures
import time
from datetime import datetime, date
import grpc

#from reputation_base_api import *
sys.path.append("./service_spec")
from reputation import ReputationAdapter

import service_spec.reputation_pb2 as pb2
import service_spec.reputation_pb2_grpc as pb2_grpc

RESP_OK = "OK"
RESP_FAIL = "FAIL"

class ReputationFeed():
    # these methods would have the grpc implementation of the Reputation System instead of testing functions. 
    def __init__(self):
        self.reputation = ReputationAdapter()
        
    def createSession(self):
        r = self.reputation.create_session()
        if r == "Ok":
            return pb2.Response(text=RESP_OK)
        else:
            return pb2.Response(text=RESP_FAIL)        
        #return self.reputation.create_session()
        
    def closeSession(self):
        r = self.reputation.close_session()
        if r == "Ok":
            return pb2.Response(text=RESP_OK)
        else:
            return pb2.Response(text=RESP_FAIL)
        
    def req(self, req):
        r = self.reputation.request(pb2.Input(req))
        if r == "Ok":
            return pb2.Response(text=RESP_OK)
        else:
            return pb2.Response(text=RESP_FAIL)
        
    def reputationRequest(self, req):
        r = self.reputation.reputation_request(pb2.Input(req))
        if r == "Ok":
            return pb2.Response(text=RESP_OK)
        else:
            return pb2.Response(text=RESP_FAIL)
    
    def setParameters(self, req):
        parameters = {['default'] : req.default, ['decayed'] : req.decayed, ['conservatism'] : req.conservatism, 
                      ['precision'] : req.precision, ['liquid'] : req.liquid, ['period'] : req.period,
                      ['aggregation'] : req.aggregation, ['downrating'] : req.downrating, ['fullnorm'] : req.fullnorm,
                      ['weighting'] : req.weighting, ['denomination'] : req.denomination, ['logratings'] : req.logratings,
                      ['ratings'] : req.ratings, ['spendings'] : req.spendings, ['parents'] : req.parents, ['predictiveness'] : req.predictiveness,
                      ['rating_bias'] : req.rating_bias, ['unrated'] : req.unrated}
        r = self.reputation.set_parameters(pb2.Param(parameters))
        if r == "Ok":
            return pb2.Response(text=RESP_OK)
        else:
            return pb2.Response(text=RESP_FAIL)
        
    def getParameters(self):
        r = self.reputation.get_parameters()
        return pb2.Param(default = r['default'], decayed = r['decayed'], conservatism = r['conservatism'], precision = r['precision'],
                       liquid = r['liquid'], period = r['update_period'], aggregation = r['aggregation'], downrating = r['downrating'], 
                       fullnorm = ['fullnorm'], weighting = r['weighting'], denomination = r['denomination'], 
                       logratings = r['logratings'], ratings = r['ratings'], spendings = r['spendings'], parents = r['parents'], 
                       predictiveness = r['predictiveness'], rating_bias = r['rating_bias'], unrated = r['unrated'])

    def setParent(self, parent): #parent_id, list_of_children_ids):
        parent_id = parent.parent_id
        child_id = parent.child_id
        r = self.reputation.set_parent(parent_id, child_id)
        if r == "Ok":
            return pb2.Response(text=RESP_OK)
        else:
            return pb2.Response(text=RESP_FAIL)
        
    def putRanks(self, rank): #date, ranks):
        date = rank.date
        ranks = rank.ranks
        r = self.reputation.put_ranks(date, ranks)
        if r == "Ok":
            return pb2.Response(text=RESP_OK)
        else:
            return pb2.Response(text=RESP_FAIL)

    def getRanks(self, req):
        r = self.reputation.get_ranks({'date' : req.date, 'ids' : req.ids})
        if r == "Ok":
            return pb2.Response(text=RESP_OK)
        else:
            return pb2.Response(text=RESP_FAIL)
    
    def clearRanks(self):
        r = self.reputation.clear_ranks()
        if r == "Ok":
            return pb2.Response(text=RESP_OK)
        else:
            return pb2.Response(text=RESP_FAIL)
        
    def updateRanks(self, req):
        date = req.date
        r = self.reputation.update_ranks(date)        
        if r == "Ok":
            return pb2.Response(text=RESP_OK)
        else:
            return pb2.Response(text=RESP_FAIL)    
            
    def putRatings(self, ratings):
        r = self.reputation.put_ratings(ratings)
        if r == "Ok":
            return pb2.Response(text=RESP_OK)
        else:
            return pb2.Response(text=RESP_FAIL)
        
    def getRatings(self, req):
        r = self.reputation.get_ratings({'since' : req.since, 'until' : req.until, 'ids' : req.ids})
        if r == "Ok":
            return pb2.Response(text=RESP_OK)
        else:
            return pb2.Response(text=RESP_FAIL)
        return self.reputation.get_ratings(filter)
        
    def clearRatings(self):
        r = self.reputation.clear_ratings()
        if r == "Ok":
            return pb2.Response(text=RESP_OK)
        else:
            return pb2.Response(text=RESP_FAIL)
        
def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ReputationFeedServicer_to_server(ReputationFeed(), server)
    server.add_insecure_port('[::]:9998')
    server.start()
    print("Server listening on 0.0.0.0:{}".format(9998))
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        server.stop(0)
    
if __name__ == '__main__':
    main()