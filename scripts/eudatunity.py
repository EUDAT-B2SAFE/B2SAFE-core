# !/usr/bin/env python

import sys
import json
import urllib2
import base64

class EudatRemoteSource:
    def _debugMsg(self, method, msg):
        """Internal: Print a debug message if debug is enabled.

        """
        if self.debug:
            print "[", method, "]", msg

    def __init__(self,host,username,password):
        self.host = host
        self.username = username
        self.password = password

    def queryUnity(self, sublink):
        """
        :param argument: url to unitydb with entity (entityID) or group (groupName)
        :return:
        """
        auth = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
        header = "Basic %s" % auth
        url = self.host + sublink
        request = urllib2.Request(url)
        request.add_header("Authorization",header)
        try:
            response = urllib2.urlopen(request)
        except IOError, e:
            print "Wrong username or password"
            sys.exit(1)

        assert response.code == 200
        json_data = response.read()
        response_dict = json.loads(json_data)

        return response_dict

