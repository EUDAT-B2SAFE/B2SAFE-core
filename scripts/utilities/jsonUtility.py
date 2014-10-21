#!/usr/bin/env python
# -*- python -*-

import subprocess
import logging


################################################################################
# JSON Utility Class #
################################################################################
 
class JSONUtils():
    """ 
    utility for json management
    """

    def __init__(self):
        """initialize the object"""


    def _decode_list(self,data):
            rv = []
            for item in data:
                if isinstance(item, unicode):
                    item = item.encode('utf-8')
                elif isinstance(item, list):
                    item = self._decode_list(item)
                elif isinstance(item, dict):
                    item = self.decode_dict(item)
                rv.append(item)
            return rv
 
 
    def decode_dict(self,data):
            rv = {}
            for key, value in data.iteritems():
                if isinstance(key, unicode):
                    key = key.encode('utf-8')
                if isinstance(value, unicode):
                    value = value.encode('utf-8')
                elif isinstance(value, list):
                    value = self._decode_list(value)
                elif isinstance(value, dict):
                    value = self.decode_dict(value)
                rv[key] = value
            return rv