import os
from pathlib import Path

class ReputationSettings():
    def __init__(self, **custom_settings):
        self.AIGENTS_PATH = 'https://aigentrep.icog-labs.com/al'
        self.AIGENTS_LOGIN_EMAIL = 'eskender@singularitynet.io'
        self.AIGENTS_LOGIN_NAME = 'test'
        self.AIGENTS_LOGIN_SURNAME = 'Aigents'
        self.AIGENTS_SECRET_QUESTION = 'favorite league'
        self.AIGENTS_SECRET_ANSWER = 'bundesliga'
        self.AIGENTS_RESP_OK = "Ok. "
        self.AIGENTS_RESP_FAIL = ["Nothing.", "No answer."]
        self.AIGENTS_FORMATS = ["text", "json", "html"]
        self.VERBOSE = False
        super().__init__(**custom_settings)