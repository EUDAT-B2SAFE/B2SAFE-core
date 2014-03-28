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
            print "problem while reading configuration file %s" % (self.file)
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
    message = queue.pop()
    print message
    queue.close()
    
def test(args):
    '''do a series of tests'''
    
    def read_log_last_line(logger, logfile):
        '''local helper func: read the last line of the log file'''
        
        logger.info('test log message')
        
        try:
            filehandle = open(logfile, "r")
            line = filehandle.readline()
            filehandle.close()
        except (OSError, IOError) as e:
            print "problem while reading file %s" % (file)
            print "Error:", e
            return False
        
        if 'test log message' in line:
            return True
        
        return False

    def test_result(result, testval):
        '''local helper func: print OK/FAIL for test result
        Returns 0 on OK, 1 on failure'''
        
        if type(result) != type(testval):
            print "FAIL (wrong type; test is bad)"
            return 1
            
        if result == testval:
            print "OK"
            return 0
        else:
            print "FAIL"
            return 1
            
    logManager = LogManager(args.conffilepath, args.debug)
    logManager.initializeLogger()
    logger = logManager.getLogger()
    logfile = logManager.getLogFile()
    logManager.initializeQueue()
    queue = logManager.getQueue()
    
    fail = 0
    
    print
    print "logging info to the file " + file
    fail += test_result(read_log_last_line(logger, logfile), True)
    print
    print "pushing info to the queue"
    queue.push('test message')
    fail += test_result('test message', queue.pop())
    queue.close()
    
    print
    if fail == 0:
        print "All tests passed OK"
    else:
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

    parser_read = subparsers.add_parser('log', help='log a message')
    parser_read.add_argument("level", help='the value of the log level')
    parser_read.add_argument("message", nargs='+', 
                             help='the message to be logged')
    parser_read.set_defaults(func=log)
    
    parser_read = subparsers.add_parser('push', help='push a message')
    parser_read.add_argument("message", nargs='+', 
                             help='the message to be queued')
    parser_read.set_defaults(func=push)
    
    parser_read = subparsers.add_parser('pop', help='pop a message')
    parser_read.set_defaults(func=pop)

    parser_test = subparsers.add_parser('test', help='Run test suite')
    parser_test.set_defaults(func=test)

    _args = parser.parse_args()
    _args.func(_args)
