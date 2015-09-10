#!/usr/bin/env python

import dweepy
import argparse
import sys
import logging
import logging.handlers
import json

logger = logging.getLogger('messageManager')

def send(args):
    """write the message to the queue"""
    msgList = (' '.join(args.message)).split(";")
    payLoad = []
    for msg in msgList:
        logger.debug('Message: ' + msg)
        payLoad.append(msg)
    logger.debug('Payload: ' + json.dumps(payLoad))
    jsonPayLoad = {'message': payLoad}
    logger.info('Dweeting to ' + args.queue)
    try:
        dweepy.dweet_for(args.queue, jsonPayLoad)
    except dweepy.DweepyError as e:
        logger.exception('Failed dweeting')
        exit(1)

def getlast(args):
    """get the last message from the queue"""
    logger.info('Getting the last message from %s', args.queue)
    try:
        jsonPayLoad = dweepy.get_latest_dweet_for(args.queue)
    except dweepy.DweepyError as e:
        logger.exception('Failed to get the last message from queue %s', 
                          args.queue)
        exit(1)
    print json.dumps({jsonPayLoad[0]['created']:
                      jsonPayLoad[0]['content']['message']})

def getall(args):
    """get all the messages from the queue"""
    logger.info('Getting all the messages from %s', args.queue)
    try:
        jsonPayLoad = dweepy.get_dweets_for(args.queue)
    except dweepy.DweepyError as e:
        logger.exception('Failed to get all the message from queue %s', 
                          args.queue)
        exit(1)
    payLoad = {}
    for message in jsonPayLoad:
        payLoad[message['created']] = message['content']['message']
    print json.dumps(payLoad)

def _initializeLogger(args):
    """initialize the logger instance."""

    if (args.debug):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    if (args.log):
        han = logging.handlers.RotatingFileHandler(args.log,
                                                   maxBytes=6000000, 
                                                   backupCount=9)
    else:
        han = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
    han.setFormatter(formatter)
    logger.addHandler(han)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='EUDAT message manager.')

    parser.add_argument("-l", "--log", help="Path to the log file")
    parser.add_argument("-d", "--debug", help="Show debug output", 
                        action="store_true")

    subparsers = parser.add_subparsers(title='Actions',
                                       description='Handle message management',
                                       help='Additional help')

    parser_send = subparsers.add_parser('send', help='send a message')
    parser_send.add_argument("queue", help='the value of the message queue')
    parser_send.add_argument("message", nargs='+', help='the message content')
    parser_send.set_defaults(func=send)

    parser_getlast = subparsers.add_parser('getlast', help='get the last message')
    parser_getlast.add_argument("queue", help='the value of the message queue')
    parser_getlast.set_defaults(func=getlast)

    parser_getall = subparsers.add_parser('getall', help='get all the messages')
    parser_getall.add_argument("queue", help='the value of the message queue')
    parser_getall.set_defaults(func=getall)

    _args = parser.parse_args()
    _initializeLogger(_args)
    _args.func(_args)
