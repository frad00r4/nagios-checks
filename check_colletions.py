#!/usr/bin/env python
# -*- coding: utf-8 -*-

# check mongodb database.
# if remove shard from cluster. need restart mongos, else may be errors.


import sys
from optparse import OptionParser

try:
    import pymongo
except ImportError, e:
    print e
    sys.exit(2)

def main():
    parser = OptionParser()
    parser.add_option('-D', '--database', action='store', type='string', dest='database', default='test', help='Database')
    parser.add_option('-H', '--host', action='store', type='string', dest='host', default='127.0.0.1', help='The hostname you want to connect to')
    parser.add_option('-P', '--port', action='store', type='int', dest='port', default=27017, help='The port mongodb is runnung on')
    (options, args) = parser.parse_args()

    try:
        conn = pymongo.MongoClient(options.host, options.port, socketTimeoutMS=30000, connectTimeoutMS=30000)
    except Exception, e:
        print e
        return 2

    db = pymongo.database.Database(conn , u'{0}'.format(options.database))
    try:
        db.collection_names()
    except:
        return 2

    print 'All OK'
    return 0;


# start script
if __name__ == "__main__":
    sys.exit(main())
