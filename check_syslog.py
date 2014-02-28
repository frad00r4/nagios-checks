#!/usr/bin/env python
# -*- coding: utf-8 -*-

# check syslog write time

import sys
import time
import syslog
from optparse import OptionParser


def main():
    parser = OptionParser()
    parser.add_option('-W', '--warning', action='store', dest='warning', default=100, type='int', help='The warning threshold we want to set')
    parser.add_option('-C', '--critical', action='store', dest='critical', default=200, type='int', help='The critical threshold we want to set')
    (options, args) = parser.parse_args()

    start = time.time()

    # syslog check start
    syslog.openlog( 'check_syslog' )
    syslog.syslog( syslog.LOG_DEBUG, 'Nagion syslog check' )
    syslog.closelog()
    # syslog check stop

    stop = time.time()
    result = int((stop - start) * 1000)
    if(result < options.warning):
        print "OK - %d ms" % result
        return 0
    if(result < options.critical):
        print "WARNING - %d ms" % result
        return 1
    else:
        print "CRITICAL - %d ms" % result
        return 2

# start script
if __name__ == "__main__":
    sys.exit(main())
