#!/usr/bin/env python

import requests
import sys
import logging
import logging.handlers
import json
import base64
import argparse
import ConfigParser
import hashlib

logger = logging.getLogger('messageManager')
session = requests.Session()

class Configuration():
    """ 
    Get properties from filesystem
    """

    def __init__(self, file, logger):

        self.file = file
        self.log_level = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG, \
                          'ERROR': logging.ERROR, 'WARNING': logging.WARNING, \
                          'CRITICAL': logging.CRITICAL}


    def parseConf(self):
        """Parse the configuration file."""

        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(open(self.file))
        # logging parameters
        logfilepath = self._getConfOption('Logging', 'log_file')
        loglevel = self._getConfOption('Logging', 'log_level')
        logger.setLevel(self.log_level[loglevel])
        rfh = logging.handlers.RotatingFileHandler(logfilepath, \
                                                   maxBytes=8388608, \
                                                   backupCount=9)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: '
                                    + '[%(funcName)s] %(message)s')
        rfh.setFormatter(formatter)
        logger.addHandler(rfh)
        # details for the connection
        self.payload = self._getConfOption('Connector', 'key')
        self.endpoint = self._getConfOption('Connector', 'endpoint')


    def _getConfOption(self, section, option, boolean=False):
        """
        get the options from the configuration file
        """

        if (self.config.has_option(section, option)):
            opt = self.config.get(section, option)
            if boolean:
                if opt in ['True', 'true']: return True
                else: return False
            return opt
        else:
            logger.warning('missing parameter %s:%s' % (section,option))
            return None

###############################################################################
# Command Line Interface #
###############################################################################

def listTopics():

    logger.info('Getting the list of topics from {}'.format(endpoint))
    headers = {'Accept': 'application/json'}
    data = {}
    res = session.get(endpoint + '/topics',
                      data=data, headers=headers, params=payload)
    logger.debug('Status code: {}'.format(str(res.status_code)))
    logger.debug('Response: {}'.format(res.text))
    return res.text
    

def createTopic(name):

    logger.info('Defining the new topic {}'.format(name))
    headers = {'Accept': 'application/json'}
    data = {}
    res = session.put(endpoint + '/topics/' + name.strip(),
                      data=data, headers=headers, params=payload)
    logger.debug('Status code: {}'.format(str(res.status_code)))
    logger.debug('Response: {}'.format(res.text))
    if res.status_code == 409:
        return name.strip()
    resJson = json.loads(res.text)
    return resJson['name'].rsplit('/',1)[1]


def deleteTopic(name):

    logger.info('Deleting the topic {}'.format(name))
    headers = {'Accept': 'application/json'}
    res = session.delete(endpoint + '/topics/' + name.strip(),
                         headers=headers, params=payload)
    logger.debug('Status code: {}'.format(str(res.status_code)))
    logger.debug('Response: {}'.format(res.text))
    return res.text


def listSub():

    logger.info('Listing the subscriptions')
    headers = {'Content-Type': 'application/json'}
    res = session.get(endpoint + '/subscriptions',
                      headers=headers, params=payload)
    logger.debug('Status code: {}'.format(str(res.status_code)))
    logger.debug('Response: {}'.format(res.text))
    return res.text


def createSub(name, topic):

    logger.info('Defining the new subscription {} for the topic {}'.format(name,
                                                                           topic))
    headers = {'Content-Type': 'application/json'}
    data = {'topic': 'projects/EUDAT2020/topics/' + topic, 'ack': '20'}
    putdata = json.dumps(data)
    res = session.put(endpoint + '/subscriptions/' + name.strip(),
                      data=putdata, headers=headers, params=payload)
    logger.debug('Status code: {}'.format(str(res.status_code)))
    logger.debug('Response: {}'.format(res.text))
    return res.text


def deleteSub(name):

    logger.info('Deleting the subscription {}'.format(name))
    headers = {'Content-Type': 'application/json'}
    res = session.delete(endpoint + '/subscriptions/' + name.strip(),
                      headers=headers, params=payload)
    logger.debug('Status code: {}'.format(str(res.status_code)))
    logger.debug('Response: {}'.format(res.text))
    return res.text    


def pubMessage(args):

    msg = ' '.join(args.message)
    logger.info('Publishing the message [{}] to the topic {}'.format(msg,
                                                                     args.topic))
    headers = {'Accept': 'application/json'}
    data = {
            'messages': [
                            { 'attributes': {},
                              'data': base64.standard_b64encode(msg)
                            }
                        ]
           }
    postdata = json.dumps(data)
    res = session.post(endpoint + '/topics/' + args.topic.strip() + ':publish',
                       data=postdata, headers=headers, params=payload)
    logger.debug('Request URL: {}'.format(res.url))
    logger.debug('Request data: {}'.format(str(data)))
    logger.debug('Status code: {}'.format(str(res.status_code)))
    logger.debug('Response: {}'.format(res.text))
    print res.text


def pullMessage(args):

    logger.info('Reading {} messages from subscription {}'.format(args.number,
                                                                  args.sub))
    headers = {'Content-Type': 'application/json'}
    data = {'maxMessages': args.number}
    postdata = json.dumps(data)
    res = session.post(endpoint + '/subscriptions/' + args.sub.strip() + ':pull',
                       data=postdata, headers=headers, params=payload)
    logger.debug('Status code: {}'.format(str(res.status_code)))
    logger.debug('Response: {}'.format(res.text))
    res_dict = json.loads(res.text)
    dataids = {'ackIds': []}
    for rmessage in res_dict['receivedMessages']:
        content = base64.standard_b64decode(rmessage['message']['data'])
        print '[{}] {}'.format(rmessage['message']['messageId'], content)
        dataids['ackIds'].append(rmessage['ackId'])
    logger.debug('Removing messages')
    postdataids = json.dumps(dataids)
    resids = session.post(endpoint + '/subscriptions/' + args.sub.strip() 
                          + ':acknowledge', data=postdataids, headers=headers, 
                          params=payload)
    logger.debug('Status code: {}'.format(str(resids.status_code)))
    logger.debug('Response: {}'.format(resids.text))
    

def manageTopic(args):

    if args.action == 'list':
        print listTopics()
    elif args.name is not None:
        name = args.name 
        if args.md5hash:
            name = hashlib.md5(args.name).hexdigest()
        if args.action == 'create':
            print createTopic(name)
        elif args.action == 'delete':
            print deleteTopic(name)
    else:
        print 'topic name is missing'


def manageSubscription(args):

    args_dict = vars(args)
    if args.action == 'list':
        print listSub()
    else:
        if not ('name' in args_dict.keys()):
            print 'subscription name is missing'
            sys.exit(1)
        if args.action == 'delete':
            print deleteSub(args.name)
            sys.exit(0)
        if not ('topic' in args_dict.keys()):
            print 'topic name is missing'
            sys.exit(1)
        topicName = args.topic
        if args.md5hash:
            topicName = hashlib.md5(args.name).hexdigest()    
        if args.action == 'create':
            print createSub(args.name, topicName)


def _initializeLogger(args):
    """initialize the logger instance."""

    if (args.debug):
        logger.setLevel(logging.DEBUG)
    if (args.log):
        han = logging.handlers.RotatingFileHandler(args.log,
                                                   maxBytes=6000000,
                                                   backupCount=9)
        formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
        han.setFormatter(formatter)
        logger.addHandler(han)


def _setToControlQueue(queue):
    """add the new queue to the control queue."""

       


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='EUDAT B2SAFE message manager.')

    parser.add_argument("conf", help="Path to the configuration file")
    parser.add_argument("-l", "--log", help="Path to the log file")
    parser.add_argument("-d", "--debug", help="Show debug output",
                        action="store_true")

    subparsers = parser.add_subparsers(title='Actions',
                                       description='Handle message management',
                                       help='Additional help')

    parser_publish = subparsers.add_parser('publish', help='post a message')
    parser_publish.add_argument("topic", help='the message topic')
    parser_publish.add_argument("message", nargs='+', help='the message content')
    parser_publish.set_defaults(func=pubMessage)

    parser_pull = subparsers.add_parser('pull', help='get messages')
    parser_pull.add_argument("number", help='the number of messages to get')
    parser_pull.add_argument("sub", help='the message subscription')
    parser_pull.set_defaults(func=pullMessage)

    parser_topic = subparsers.add_parser('topic', help='topic management')
    parser_topic.add_argument("action", choices=['list', 'create', 'delete'], 
                              help='topic action')
    parser_topic.add_argument("name", nargs='?', default=argparse.SUPPRESS, 
                              help='topic name for create and delete actions')
    parser_topic.add_argument("-m", "--md5hash", help="create the topic using"
                             + " the md5 hash of the name", action="store_true")
    parser_topic.set_defaults(func=manageTopic)

    parser_sub = subparsers.add_parser('sub', help='subscription management')
    parser_sub.add_argument("action", choices=['list', 'create', 'delete'],  
                            help='subscription action')
    parser_sub.add_argument("name", nargs='?', default=argparse.SUPPRESS, 
                            help='subscription name for create and delete actions')
    parser_sub.add_argument("topic", nargs='?', default=argparse.SUPPRESS,
                            help='topic name for create action')
    parser_sub.add_argument("-m", "--md5hash", help="the topic real name is"
                           + " the md5 hash of the name", action="store_true") 
    parser_sub.set_defaults(func=manageSubscription)  

    _args = parser.parse_args()
    configuration = Configuration(_args.conf, logger)
    configuration.parseConf()
    payload = {'key': configuration.payload}
    endpoint = configuration.endpoint
    _initializeLogger(_args)
    _args.func(_args)
