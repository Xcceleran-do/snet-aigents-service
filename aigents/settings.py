import os
from pathlib import Path

DEMO_PARENT_DIR = Path(__file__).parent.parent.parent


class AigentsSettings():
    def __init__(self, **custom_settings):
        if os.getenv("AIGENTS_PROD_ENV") and \
           os.getenv("AIGENTS_PROD_ENV") == "1":
            self._ENV_PREFIX = 'SN_AIGENTS_PROD'
            self.AIGENTS_PATH = 'https://aigents.singularitynet.io/69616567746e6c736e610067'
            self.AIGENTS_LOGIN_EMAIL = 'test@singularitynet.io'
            self.AIGENTS_LOGIN_NAME = 'Test'
            self.AIGENTS_LOGIN_SURNAME = 'Aigents'
            self.AIGENTS_SECRET_QUESTION = 'purpose'
            self.AIGENTS_SECRET_ANSWER = 'testing'
        else:
            self._ENV_PREFIX = 'SN_AIGENTS_DEV'
            self.AIGENTS_PATH = 'https://aigents.icog-labs.com/69616567746e6c736e610067'
            self.AIGENTS_LOGIN_EMAIL = 'test@icog-labs.com'
            self.AIGENTS_LOGIN_NAME = 'Test'
            self.AIGENTS_LOGIN_SURNAME = 'Aigents'
            self.AIGENTS_SECRET_QUESTION = 'abebe'
            self.AIGENTS_SECRET_ANSWER = 'beso'

        self.AIGENTS_RESP_OK = "Ok. "
        self.AIGENTS_RESP_FAIL = ["No thing.", "There not."]
        self.AIGENTS_FORMATS = ["text", "json", "html"]

        super().__init__(**custom_settings)
