import unittest
from logmanager import LogManager

__author__ = 'lphan'


class LogManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.confpath = self._getconfigpath()

    def tearDown(self):
        pass

    def _getconfigpath(self):
        fobj = open("testB2SafeCmd.conf", "r")
        lines = fobj.readlines()
        for line in lines:
            if line.find('LOG_PATH') > -1:
                configpath = line.split()
        fobj.close()
        return configpath[1]

    def _read_log_last_line(self, logger, logfile):
        '''local helper func: read the last line of the log file'''

        logger.info('test log message')

        try:
            filehandle = open(logfile, "r")
            # read last line in file
            linelist = filehandle.readlines()
            filehandle.close()
        except (OSError, IOError) as er:
            print "problem while reading file %s" % logfile
            print "Error:", er
            return False
        #print linelist
        lastline = linelist[len(linelist)-1]
        if 'test log message' in lastline:
            return True

        return False

    def test_case(self):
        print "Get config file log.manager.conf from testB2SafeCmd.conf"
        print "Check Config Path = ", self.confpath

        try:
            logmanager = LogManager(self.confpath, "")
            logmanager.initializeLogger()
            logger = logmanager.getLogger()
            logfile = logmanager.getLogFile()
        except IOError as er:
            print "IOError, directory 'log' might not exist"
            print "Error: ", er
            return False

        logmanager.initializeQueue()
        queue = logmanager.getQueue()

        print
        print "Case 1: log message"
        self.assertTrue(self._read_log_last_line(logger, logfile))

        print
        print "Case 2: push message in queue"
        queue.push("test-message")

        print
        print "Case 3: check queue size (should be 1)"
        self.assertEqual(len(queue), 1)

        print
        print "Case 4: push message in queue"
        queue.push("test-message-2")

        print
        print "Case 5: check queue size, again (should be 2)"
        self.assertEqual(len(queue), 2)

        print
        print "Case 6: pop message from queue (should be test-message)"
        self.assertEqual(queue.pop(), "test-message")

        print
        print "Case 7: check queue size, again (should be 1)"
        self.assertEqual(len(queue), 1)

        print
        print "Case 8: pop message from queue, again (should be test-message-2)"
        self.assertEqual(queue.pop(), "test-message-2")

        print
        print "Case 9: check queue size last time (should be 0)"
        self.assertEqual(len(queue), 0)