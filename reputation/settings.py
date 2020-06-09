import os
from pathlib import Path

DEMO_PARENT_DIR = Path(__file__).parent.parent.parent

class ReputationSettings():
    def __init__(self, **custom_settings):
        if os.getenv("AIGENTS_PROD_ENV") and \
           os.getenv("AIGENTS_PROD_ENV") == "1":
            self._ENV_PREFIX = 'SN_AIGENTS_PROD'
            self.AIGENTS_PATH = 'https://aigents.singularitynet.io/69616567746e6c736e610067'
            self.AIGENTS_LOGIN_EMAIL = 'dagim@singularitynet.io'
            self.AIGENTS_LOGIN_NAME = 'dagim'
            self.AIGENTS_LOGIN_SURNAME = 'sisay'
            self.AIGENTS_SECRET_QUESTION = 'abebe'
            self.AIGENTS_SECRET_ANSWER = 'beso'
        else:
            self._ENV_PREFIX = 'SN_AIGENTS_DEV'
            self.AIGENTS_PATH = 'https://aigents.icog-labs.com/69616567746e6c736e610067'
            self.AIGENTS_LOGIN_EMAIL = 'dagim@singularitynet.io'
            self.AIGENTS_LOGIN_NAME = 'dagim'
            self.AIGENTS_LOGIN_SURNAME = 'sisay'
            self.AIGENTS_SECRET_QUESTION = 'abebe'
            self.AIGENTS_SECRET_ANSWER = 'beso'
            
        self.AIGENTS_RESP_OK = "Ok. "
        self.AIGENTS_RESP_FAIL = ["Nothing.", "No answer."]
        self.AIGENTS_FORMATS = ["text", "json", "html"]
        self.VERBOSE = False
        
        super().__init__(**custom_settings)