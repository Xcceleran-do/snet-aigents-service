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
        print("Aigents Running Mode: ", self.settings._ENV_PREFIX)
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

    def aigents_signup(self, f_name, l_name, email, sec_q, sec_a):
        r = self.request("logout")
        r = self.request("my email " + email
                       + ", name " + f_name
                       + ", surname " + l_name
                       + ", secret question " + sec_q
                       + ", secret answer " + sec_a)
        if r.lower() == "what your " + sec_q.lower() + "?":
            r = self.request("my " + sec_q + " " + sec_a)
        else:
            return AIGENTS_RESP_FAIL

        if r.find(self.settings.AIGENTS_RESP_OK + "Hello") == -1:
            return AIGENTS_RESP_FAIL
        self.aigents_set_format("json")
        return AIGENTS_RESP_OK

    def aigents_login(self, email, sec_q, sec_a):
        r = self.request("logout")
        r = self.request("my email " + email)
        if r.lower() == "what your " + sec_q.lower() + "?":
            r = self.request(sec_a)
        else:
            return AIGENTS_RESP_FAIL
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
        self.aigents_set_format("json")
        r = self.request("what my email?")
        return json.loads(r)[0]["email"]

    def aigents_add_topic(self, pattern):
        r = self.request("my topics '" + pattern + "', trusts '" + pattern + "'")
        return r

    def aigents_add_site(self, site):
        r = self.request("my sites '" + site + "', trusts '" + site + "'")
        return r

    def aigents_remove_topic(self, pattern):
        r = self.request("name '" + pattern + "' trust false")
        return r

    def aigents_remove_site(self, site):
        r = self.request("my sites no '" + site + "' ignores '" + site + "'")
        return r

    def aigents_create_news_item(self, title, date, url, img_url):
        r = self.request("There text '" + title + "', sources '"
                         + url + "', times " + date + ", new true,"
                         + "trust true update")
        return r

    def aigents_vote_on_item(self, title, date, url, vote):
        req = "sources '" + url + "' and text '" \
              + title + "' and times " + date + " trust "
        req += "true" if vote else "false"
        r = self.request(req)
        return r

    def aigents_rm_news_item(self, title, date, url):
        r = self.request("Sources '" + url + "' and text '"
                         + title + "' and times " + date + " new false")
        return r

    def aigents_friend(self, email, friend):
        req = "is peer and email '" + email + "' friend "
        req += "true" if friend else "false"
        r = self.request(req)
        return r

    def aigents_get_peer_name(self, email):
        self.aigents_set_format("json")
        r = self.request("what is peer, email " + email
                       + " name, surname?")
        j = json.loads(r)[0]
        return j['name'], j['surname']

    def aigents_peer_share(self, email, share):
        if share:
            self.aigents_friend(email, True)
        name, surname = self.aigents_get_peer_name(email)
        req = "is peer, name '" + name + "' and email '" + email + "' share "
        req += "true" if share else "false"
        r = self.request(req)
        return r

    def aigents_peer_receive(self, email, receive):
        if receive:
            self.aigents_friend(email, True)
        name, surname = self.aigents_get_peer_name(email)
        req = "is peer, name '" + name + "' and email '" + email + "' trust "
        req += "true" if receive else "false"
        r = self.request(req)
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
