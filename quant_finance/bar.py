#coding: utf8

from kuankr_utils import log, debug
from kuankr_utils.open_struct import DefaultOpenStruct


class InvalideBar(StandardError):
    pass
    
class Bar(DefaultOpenStruct):
    defaults = {
        'symbol': None,
        'open': None,
        'high': None,
        'low': None,
        'close': None,
        'time': None,
        'volume': 0,
        'amount': 0,
    }
    def validate(bar):
        pass


