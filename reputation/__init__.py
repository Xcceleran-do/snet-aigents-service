# MIT License
#
# Copyright (c) 2018-2019 Stichting SingularityNET
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Reputation Service wrapper around Aigents Java-based Web Service
"""

import sys
import urllib.parse
import requests
import logging
import logging.handlers as loghandlers
from reputation_base_api import *

import logging
import logging.handlers as loghandlers
logger = logging.getLogger(__name__)
from settings import ReputationSettings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
loghandle = loghandlers.TimedRotatingFileHandler(
                filename="reputation-adapter.log",
                when='D', interval=1, backupCount=7,
                encoding="utf-8")
loghandle.setFormatter(
    logging.Formatter("%(asctime)s %(message)s"))
logger.addHandler(loghandle)

AIGENTS_RESP_OK = "OK"
AIGENTS_RESP_FAIL = "FAIL"

class ReputationAdapter(ReputationServiceBase):
    type_name = "ReputationAdapter"

    def __init__(self):
        self.real_mode = True
        self.verbose = True
        self.settings = ReputationSettings()
        self.name = self.settings.AIGENTS_LOGIN_NAME
        self.verbose = False
        ReputationServiceBase.__init__(self, self.name, self.verbose)
        self.base_url = self.settings.AIGENTS_PATH
        self.login_email = self.settings.AIGENTS_LOGIN_EMAIL
        self.secret_question = self.settings.AIGENTS_SECRET_QUESTION 
        self.secret_answer = self.settings.AIGENTS_SECRET_ANSWER 
        self.create_session()
        self.request('Your retention period 3650.')
        
    def create_session(self):
        self.session = requests.session()
        if self.real_mode:
            # TODO assertions
            self.request('my email ' + self.login_email + '.')
            self.request('my ' + self.secret_question +
                            ' ' + self.secret_answer + '.')
            self.request('my language english.')
            return AIGENTS_RESP_OK
        else:
            # TODO make sure if we can use only one of these
            output = self.request('my name ' + self.login_email + ', surname ' +
                                    self.login_email + ', email ' + self.login_email + '.')
            if output == 'What your secret question, secret answer?':
                self.request(
                    'my secret question ' + self.secret_question + ', secret answer ' + self.secret_answer + '.')
            output = self.request(
                'my ' + self.secret_question + ' ' + self.secret_answer + '.')
            if output.split()[0] == 'Ok.':
                return AIGENTS_RESP_OK
            else:
                return AIGENTS_RESP_FAIL            
    
    def close_session(self):
        if not self.real_mode:
            self.request('Your trusts no ' + self.login_email + '.')
            self.request('No name ' + self.login_email + '.')
            self.request('No there times today.')
        output = self.request('My logout.')
        if self.verbose:
            logger.info("Aigents session for " + self.login_email + "closed")
        return output
        
    def request(self, input):
        url = self.base_url + '?' + urllib.parse.quote_plus(input)
        try:
            r = self.session.post(url)
            if r is None or r.status_code != 200:
                logger.error('request ' + url + ' error ' + str(r.status_code))
                raise RuntimeError("Aigents - no response")
        except Exception as e:
            if self.verbose:
                logger.error('request ' + url + ' ' + str(type(e)))
            print('No connection to aigents')
            return 'No connection to Aigents, ' + str(type(e))
        if self.verbose:
            logger.info("Request: " + url)
            logger.info("Response: " + r.text)
        return r.text

    def reputation_request(self, input):
        return self.request('reputation network ' + self.name + ' ' + input)

    def set_parameters(self, parameters):
        for key in parameters:
            value = parameters[key]
            self.parameters[key] = value
        cmd = 'set parameters' \
            + ' default ' + str(self.parameters['default']) \
            + ' decayed ' + str(self.parameters['decayed']) \
            + ' conservatism ' + str(self.parameters['conservatism']) \
            + ' precision ' + str(self.parameters['precision']) \
            + ' liquid ' + ('true' if self.parameters['liquid'] else 'false') \
            + ' period ' + str(self.parameters['update_period']) \
            + ' aggregation ' + ('true' if self.parameters['aggregation'] else 'false') \
            + ' downrating ' + ('true' if self.parameters['downrating'] else 'false') \
            + ' fullnorm ' + ('true' if self.parameters['fullnorm'] else 'false') \
            + ' weighting ' + ('true' if self.parameters['weighting'] else 'false') \
            + ' denomination ' + ('true' if self.parameters['denomination'] else 'false') \
            + ' logratings ' + ('true' if self.parameters['logratings'] else 'false') \
            + ' ratings ' + str(self.parameters['ratings']) \
            + ' spendings ' + str(self.parameters['spendings']) \
            + ' parents ' + str(self.parameters['parents']) \
            + ' predictiveness ' + str(self.parameters['predictiveness']) \
            + ' rating_bias ' + ('true' if self.parameters['rating_bias'] else 'false') \
            + ' unrated ' + ('true' if self.parameters['unrated'] else 'false')
        res = self.reputation_request(cmd)
        
        if res.strip() == 'Ok.':
            return AIGENTS_RESP_OK
        else:
            return AIGENTS_RESP_FAIL
        
    def get_parameters(self): 
        return self.parameters
    
    def set_parent(self, parent_id, list_of_children_ids):
        cmd = 'set parent ' + str(parent_id) 
        for id in list_of_children_ids:
            cmd += ' child ' + str(id)
        res = self.reputation_request(cmd)
        if res.strip() == 'Ok.':
            return AIGENTS_RESP_OK
        else:
            return AIGENTS_RESP_FAIL
        
    #TODO
    def clear_ranks(self):
        pass
        
    def clear_ratings(self):
        pass
        
    def get_ranks(self, filter):
        pass
    
    def get_ratings(self, filter):
        pass
    
    def put_ranks(self, date, ranking):
        pass
    
    def put_ratings(self, rating):
        pass
    
    def update_ranks(self, date):
        pass