#!/usr/bin/env python3

import sys
from concurrent import futures
import time
from datetime import datetime, date
from reputation import ReputationAdapter

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
        
    def putRanks(self, date, ranks):
        return self.reputation.put_ranks(date, ranks)

    def getRanks(self, filter):
        return self.reputation.get_ranks(filter)
    
    def clearRanks(self):
        return self.reputation.clear_ranks()
    
    def updateRanks(self, date):
        return self.reputation.update_ranks(date)    
        
    def clearRatings(self):
        return self.reputation.clear_ratings()
    
    def getRatings(self, filter):
        return self.reputation.get_ratings(filter)
    
    def putRatings(self, ratings):
        return self.reputation.put_ratings(ratings)
        
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
    dt = date(2007, 3, 9)
    dt1 = date(2018, 4, 9)
    ranks = [{'id':1,'rank':50},{'id':2,'rank':50}]
    rank_filter = {'date': dt, 'ids': '1 2'}
    ratings_filter = {'ids':['2'], 'since':dt, 'until':dt1}
    ratings = [{'from':12, 'type':'rating', 'to':2, 'value':100, 'weight':1, 'time':dt}]
    print("Response from put_ranks: ", repFeed.putRanks(dt, ranks))
    print("Response from get_ranks: ", repFeed.getRanks(rank_filter))
    print("Response from update_ranks: ", repFeed.updateRanks(dt1))
    print("Response from put_ratings: ", repFeed.putRatings(ratings))
    print("Response from get_ratings: ", repFeed.getRatings(ratings_filter))
    print("Response from clear_ratings: ", repFeed.clearRatings())    
    print("Response from clear_ranks: ", repFeed.clearRanks())
    print("Response from close_session: ", repFeed.closeSession())
    
if __name__ == '__main__':
    main()