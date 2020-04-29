#!/usr/bin/env python3

import sys
from concurrent import futures
import time
from __init__ import ReputationAdapter

class ReputationFeed():
    # these methods would have the grpc implementation of the Reputation System instead of testing functions. 
    def __init__(self):
        self.reputation = ReputationAdapter()
        
    def create_session(self):
        output = self.reputation.create_session()
        return output
    
    def close_session(self):
        output = self.reputation.close_session()
        return output
        
    def request(self, input):
        output = self.reputation.request(input)
        return output
        
    def reputation_request(self, input):
        output = self.reputation.reputation_request(input)
        return output
        
def main():
    repFeed = ReputationFeed()
    print(repFeed.request("my email?"))
    print(repFeed.reputation_request("clear ratings"))
    print(repFeed.close_session())
    
if __name__ == '__main__':
    main()