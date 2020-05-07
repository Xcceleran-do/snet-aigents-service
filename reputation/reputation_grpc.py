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