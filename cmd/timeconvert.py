#!/usr/bin/env python

import calendar
import datetime as DT
import sys

def epoch_to_iso8601(timestamp):
    """
    epoch_to_iso8601 - convert the unix epoch time into a iso8601 formatted date
    >>> epoch_to_iso8601(1449147762)
    '2015-12-03T13:02:42Z'
    """
    iso_time = DT.datetime.utcfromtimestamp(timestamp).isoformat()+"Z"
    print iso_time

def iso8601_to_epoch(dateTime_string):
    """
    iso8601_to_epoch - convert a iso8601 formatted date into the unix epoch time 
    >>> iso8601_to_epoch('2015-12-03T13:02:42Z')
    1449147762
    """
    epoch_time =  calendar.timegm(DT.datetime.strptime(dateTime_string, "%Y-%m-%dT%H:%M:%SZ").timetuple())
    print epoch_time

if __name__ == "__main__":

     if sys.argv[1] == 'epoch_to_iso8601':
         epoch_to_iso8601(float(sys.argv[2])) 
     elif sys.argv[1] == 'iso8601_to_epoch':
         iso8601_to_epoch(sys.argv[2])
     else:
         print "Error, not valid option"

