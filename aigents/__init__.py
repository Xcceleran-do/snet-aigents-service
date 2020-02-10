#
# agent/adapters/aigents/__init__.py - adapter integrating different sub-services of Aigents web service,
# such as RSS feeding, social graph discovery, summarizing text extraction by pattern and entity attribution
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import urllib.parse
import requests
import logging
import logging.handlers as loghandlers
import xml.etree.ElementTree as ET
import json
from typing import List

from aigents.settings import AigentsSettings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
loghandle = loghandlers.TimedRotatingFileHandler(
                filename="aigents-adapter.log",
                when='D', interval=1, backupCount=7,
                encoding="utf-8")
loghandle.setFormatter(
    logging.Formatter("%(asctime)s %(message)s"))
logger.addHandler(loghandle)

AIGENTS_RESP_OK = "OK"
AIGENTS_RESP_FAIL = "FAIL"

#TODO
"""
    - catch exception from request (broken session, no internet access...)
    - recreate session
    - rely on user format setting for parsing (assuming json for now)
    - add social media linking and news social relevance rating
"""

class AigentsAdapter():
    type_name = "AigentsAdapter"

    def __init__(self):
        self.settings = AigentsSettings()
        self.session = requests.session()
        # XXX logging in with default email for now (channel based)
        self.aigents_login(self.settings.AIGENTS_LOGIN_EMAIL,
                           self.settings.AIGENTS_SECRET_QUESTION,
                           self.settings.AIGENTS_SECRET_ANSWER)

    def request(self, request):
        url = self.settings.AIGENTS_PATH+"?"+request
        r = self.session.post(url)
        if r is None or r.status_code != 200:
            logger.error(url,r.status_code)
            raise RuntimeError("Aigents - no response")
        logger.info("Request: " + url)
        logger.info("Response: " + r.text)
        return r.text

    def validate(self, data, key):
        if not key in data or len(data[key]) < 1:
            raise RuntimeError("Aigents - no input data "+key)
        return data[key]

    def aigents_login(self, email, sec_q, sec_a):
        r = self.request("logout")
        r = self.request("my email " + email)
        # XXX check if server asked for secq-seca or name
        # simply going with secq seca for now
        r = self.request("my " + sec_q + " " + sec_a)
        if r.find(self.settings.AIGENTS_RESP_OK + "Hello") == -1:
            return AIGENTS_RESP_FAIL
        # XXX setting default format JSON
        self.aigents_set_format("json")
        return AIGENTS_RESP_OK

    def aigents_set_format(self, fmt):
        if fmt in self.settings.AIGENTS_FORMATS:
            r = self.request("my format " + fmt);
            return AIGENTS_RESP_OK
        return AIGENTS_RESP_FAIL

    def aigents_get_format(self):
        r = self.request("what my format?");
        return r

    def aigents_get_email(self):
        r = self.request("what my email?")
        return json.loads(r)[0]["email"]
    
    def aigents_set_topics(self, label, pattern):
        r = self.request("my topics " + label + ", trusts " + pattern)
        return r
    
    def aigents_set_sites(self, site):
        r = self.request("my sitess " + site + ", trusts " + site)
        return r

    def aigents_get_rss(self, channel):
        rss = self.request("rss " + channel)
        xr = ET.fromstring(rss)
        resp = []
        for item in xr.getchildren()[0].findall('item'):
            resp.append({"title" : item.find('title').text,
                         "link" : item.find('link').text,
                         "description" : item.find('description').text})
        return resp
    def aigents_get_news(self, channel):
        r = self.request("what new true sources, text, times, trust, relevance, social relevance, image, is?")
        return r
