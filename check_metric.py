#!/usr/bin/python
# -*- coding: utf-8 -*-

# check mongodb collection on change size

import sys
import json
import os
import time
from optparse import OptionParser
from pymongo import MongoClient

parser = OptionParser()
parser.add_option("-s", "--server", dest="server", help="Set server address",  metavar="ADDRESS", default=u"127.0.0.1")
parser.add_option("-p", "--port", dest="port", help="Set server port",  metavar="PORT", default=27017, type="int")
parser.add_option("-d", "--database", dest="db", help="Set database",  metavar="DATABASE", default=u"requestsdb")
parser.add_option("-c", "--collection", dest="collection", help="Set collection",  metavar="COLLECTION", default=u"metric")
parser.add_option("-f", "--historyfile", dest="file", help="Set data file",  metavar="FILENAME", default=u"/tmp/metrichistory")
parser.add_option("-i", "--interval", dest="interval", help="Set interval",  metavar="SECONDS", default=86400, type="int")
parser.add_option("-l", "--lock", dest="lock", help="Set lock file",  metavar="FILENAME", default="/tmp/")
(options, args) = parser.parse_args()

try:
    client = MongoClient(options.server, options.port, socketTimeoutMS=30000, connectTimeoutMS=30000)
except Exception as err:
    print "Metric check critical: %s" % err
    exit(2)

database = client[options.db]
collection = database[options.collection]
metr_count = collection.count()

if os.path.exists(options.file):
    mf = open(options.file, 'r')
    json_str = mf.read()
    jsdec = json.JSONDecoder()
    try:
        data_obj = jsdec.decode( json_str )
    except ValueError as err:
        mf.close()
        os.unlink(options.file)
        print "Metric check critical: %s" % err
        exit(2)
    mf.close()
    if (int(data_obj["datetime"]) + options.interval) < time.time():
        if metr_count > data_obj["count"]:
            os.unlink(options.file)
        else:
            print "Metric check critical"
            exit(2)
    else:
        print "Metric check OK"
        exit(0)

jsenc = json.JSONEncoder()
mf = open(options.file, 'w')
mf.write(jsenc.encode({"count": metr_count, "datetime": time.time()} ))
mf.close()
print "Metric check OK"
exit(0)
