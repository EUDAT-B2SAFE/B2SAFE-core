#!/usr/bin/env python
#
#   authZ.manager.py
#
#   * use 4 spaces!!! not tabs
#   * See PEP-8 Python style guide http://www.python.org/dev/peps/pep-0008/
#   * use pylint
#

"""EUDAT authorization client API.

queuelib
download from https://pypi.python.org/pypi/queuelib
python setup.py install

apt-get install pylint

"""

import argparse
import sys
import logging
import logging.handlers
from queuelib import FifoDiskQueue

###############################################################################
# Log Manager Client Class #
###############################################################################


class LogManager(object):
    """Class implementing a log manager."""

    def __init__(self, confFilePath, debug):
        """Initialize object with connection parameters."""

        self.file = confFilePath
        self.debug = debug
        self.log_level = {}
        self.log_level['DEBUG'] = logging.DEBUG
        self.log_level['INFO'] = logging.INFO
        self.log_level['WARNING'] = logging.WARNING
        self.log_level['ERROR'] = logging.ERROR
        self.log_level['CRITICAL'] = logging.CRITICAL
        self._parseConf()

    def _debugMsg(self, method, msg):
        """Internal: Print a debug message if debug is enabled."""

        if self.debug:
            print "[", method, "]", msg

    def _parseConf(self):
        """Internal: Parse the configuration file.
                     and initialize logger and queue instances"""

        try:
            filehandle = open(self.file, "r")
            tmp = eval(filehandle.read())
            filehandle.close()
        except (OSError, IOError) as e:
            print "problem while reading configuration file %s" % self.file
            print "Error:", e

        self.log_level_value = self.log_level[tmp['log_level']]
        self.log_dir = tmp['log_dir']

    def initializeLogger(self):
        """initialize the logger instance."""

        self.logger = logging.getLogger('LogManager')
        self.logger.setLevel(self.log_level_value)
        self.logfile = self.log_dir+'/b2safe.log'
        rfh = logging.handlers.RotatingFileHandler(self.logfile,
                                                   maxBytes=2097152, 
                                                   backupCount=9)
        formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
        rfh.setFormatter(formatter)
        self.logger.addHandler(rfh)

    def initializeQueue(self):
        """initialize the queue instance."""

        queuedir = self.log_dir+'/b2safe.queue'
        self.queue = FifoDiskQueue(queuedir)
        
    def getLogger(self):
        """get the logger instance."""

        return self.logger

    def getLogFile(self):
        """get the log file."""
        
        return self.logfile

    def getQueue(self):
        """get the queue instance."""
        
        return self.queue


###############################################################################
# EUDAT Log Manager Command Line Interface #
###############################################################################

def log(args):
    '''perform log action'''

    logManager = LogManager(args.conffilepath, args.debug)
    logManager.initializeLogger()
    logger = logManager.getLogger()

    msg = ' '.join(args.message)
    if args.level == 'DEBUG':
        logger.debug(msg)
    elif args.level == 'INFO':
        logger.info(msg)
    elif args.level == 'WARNING':
        logger.warning(msg)
    elif args.level == 'ERROR':
        logger.error(msg)
    elif args.level == 'CRITICAL':
        logger.critical(msg)
    else:
        sys.stdout.write('no log level defined')


def push(args):
    '''perform push action'''
    
    logManager = LogManager(args.conffilepath, args.debug)
    logManager.initializeQueue()
    queue = logManager.getQueue()
    queue.push(' '.join(args.message))
    queue.close()


def pop(args):
    '''perform pop action'''
    
    logManager = LogManager(args.conffilepath, args.debug)
    logManager.initializeQueue()
    queue = logManager.getQueue()

    if args.number:
        i = 0
        messages = []
        while i < int(args.number):
            message = queue.pop()
            if message is not None:
                messages.append(message)
            else:
                break
            i += 1
        print messages
    else:
        message = queue.pop()
        print message
        
    queue.close()


def queuesize(args):
    '''get the current size of the queue'''
    
    logManager = LogManager(args.conffilepath, args.debug)
    logManager.initializeQueue()
    queue = logManager.getQueue()
    length = str(len(queue))
    print length
    queue.close()


def test(args):
    '''do a serie of tests'''
    
    def read_log_last_line(logger, logfile):
        '''local helper func: read the last line of the log file'''
        
        logger.info('test log message')
        
        try:
            filehandle = open(logfile, "r")
            linelist = filehandle.readlines()
            filehandle.close()
        except (OSError, IOError) as er:
            print "problem while reading file %s" % logfile
            print "Error:", er
            return False
        lastline = linelist[len(linelist)-1]
        if 'test log message' in lastline:
            return True
        
        return False

    def test_result(result, testval):
        """local helper func: print OK/FAIL for test result
        Returns 0 on OK, 1 on failure"""
        
        if type(result) != type(testval):
            print "FAIL (wrong type; test is bad)"
            return 1
            
        if result == testval:
            print "OK"
            return 0
        else:
            print "FAIL"
            return 1

    try:
        logManager = LogManager(args.conffilepath, args.debug)
        logManager.initializeLogger()
        logger = logManager.getLogger()
        logfile = logManager.getLogFile()
    except IOError as er:
        print "IOError, directory 'log' might not exist"
        print "Error: ", er
        return False

    logManager.initializeQueue()
    queue = logManager.getQueue()
    
    fail = 0
    
    print
    print "logging info to the file " + logfile
    print "Test: log message"
    fail += test_result(read_log_last_line(logger, logfile), True)

    print
    print "Test: queue size before push"
    fail += test_result(len(queue), 0)

    print
    print "Test: push info to the queue"
    queue.push('test message')
    print "OK"

    print
    print "Test: queue size after push "
    fail += test_result(len(queue), 1)

    print
    print "Test: pop info from queue"
    fail += test_result('test message', queue.pop())
    
    print
    print "Test: check queue size, again (should be 0)"
    fail += test_result(len(queue), 0)

    queue.close()
    if fail == 0:
        print
        print "All tests passed OK"
    else:
        print
        print "%d tests failed" % fail


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='EUDAT log manager. ')
    parser.add_argument("conffilepath", default="NULL",
                        help="path to the configuration file")
    parser.add_argument("-d", "--debug", help="Show debug output", 
                        action="store_true")

    subparsers = parser.add_subparsers(title='Actions',
                                       description='Handle log management '
                                                   'actions',
                                       help='additional help')

    parser_log = subparsers.add_parser('log', help='log a message')
    parser_log.add_argument("level", help='the value of the log level')
    parser_log.add_argument("message", nargs='+', 
                            help='the message to be logged')
    parser_log.set_defaults(func=log)

    parser_push = subparsers.add_parser('push', help='push a message')
    parser_push.add_argument("message", nargs='+', 
                             help='the message to be queued')
    parser_push.set_defaults(func=push)

    parser_pop = subparsers.add_parser('pop', help='pop a message')
    parser_pop.add_argument("-n", "--number", help="pop a number of elements")
    parser_pop.set_defaults(func=pop)

    parser_queue = subparsers.add_parser('queuesize', help='get the length '
                                                           'of the queue')
    parser_queue.set_defaults(func=queuesize)

    parser_test = subparsers.add_parser('test', help='Run test suite')
    parser_test.set_defaults(func=test)

    _args = parser.parse_args()
    _args.func(_args)
