#!/usr/bin/env python3

import sys
from concurrent import futures
import time
from __init__ import ReputationAdapter

class ReputationFeed():
    # these methods would have the grpc implementation of the Reputation System instead of testing functions. 
    def __init__(self):
        self.reputation = ReputationAdapter()
        
    def createSession(self):
        return self.reputation.create_session()
        
    def closeSession(self):
        return self.reputation.close_session()
        
    def req(self, input):
        return self.reputation.request(input)
        
    def reputationRequest(self, input):
        return self.reputation.reputation_request(input)
    
    def setParameters(self, parameters):
        return self.reputation.set_parameters(parameters)
        
    def getParameters(self):
        return self.reputation.get_parameters()
        
    def setParent(self, parent_id, list_of_children_ids):
        return self.reputation.set_parent(parent_id, list_of_children_ids)
        
def main():
    repFeed = ReputationFeed()
    print("Response from request: ", repFeed.req("my email?"))
    print("Response from reputation_request: ", repFeed.reputationRequest("clear ratings"))
    param = {'default' : 0.0, 'decayed' : 0.5, 'conservatism' : 0.5, 'precision' : 1, 'update_period' : 1, 'aggregation' : False, 'downrating' : False,
             'ratings' : 1.0, 'spendings' : 0.0, 'parents' : 0.0, 'predictiveness' : 0.0} 
    print("Response from set_parameter: ", repFeed.setParameters(param))
    print("Response from get_parameter: ", repFeed.getParameters())
    pid = 1
    cids = [2, 3]
    print("Response from set_parent: ", repFeed.setParent(pid, cids))
    print("Response from close_session: ", repFeed.closeSession())
    
if __name__ == '__main__':
    main()