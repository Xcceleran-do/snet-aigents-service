import os
from pathlib import Path

DEMO_PARENT_DIR = Path(__file__).parent.parent.parent


class AigentsSettings():
    def __init__(self, **custom_settings):
        self._ENV_PREFIX = 'SN_AIGENTS_'
        self.AIGENTS_PATH = 'https://aigents.icog-labs.com/69616567746e6c736e610067'
        self.AIGENTS_LOGIN_EMAIL = 'aigents@icog-labs.com'
        self.AIGENTS_SECRET_QUESTION = 'abebe'
        self.AIGENTS_SECRET_ANSWER = 'beso'
        self.AIGENTS_RESP_OK = "Ok. "
        self.AIGENTS_RESP_FAIL = ["No thing.", "There not."]
        self.AIGENTS_FORMATS = ["text", "json", "html"]

        super().__init__(**custom_settings)
