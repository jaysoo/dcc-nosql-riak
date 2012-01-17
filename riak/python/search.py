#!/usr/bin/env python
import sys, pprint
import riak
from settings import settings

def query(bucket_name, field, value):
    client = riak.RiakClient(host=settings['HOST'], port=settings['PORT'], transport_class=settings['TRANSPORT_CLASS'])
    results = client.index(bucket_name, field, value).run()
    pp = pprint.PrettyPrinter(depth=6)

    for link in results:
        pp.pprint( link.get().get_data() )

if __name__ == '__main__':
    if len( sys.argv ) < 4:
        print '\033[0;31mthree arguments required\033[0m'
        sys.exit(1)

    query(sys.argv[1], sys.argv[2], sys.argv[3])


