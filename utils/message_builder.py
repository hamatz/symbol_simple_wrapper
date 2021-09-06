import json

TM_VERSION = 1
TM_PROTOCOL_NAME = 'thanks_meter'

class ThanksMessageBuilder:
    def __init__(self):
        print('Initializing ThanksMessageBuilder...')
        self._version = TM_VERSION
        self._protocol_name = TM_PROTOCOL_NAME

    def build_tm_string(self, target_address):
        message = {
            'version': self._version,
            'protocol': self._protocol_name,
            'target': target_address
        }
        return json.dumps(message)