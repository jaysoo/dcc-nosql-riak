#!/usr/bin/env python
import sys, pprint, time
import riak
from settings import settings

def query(bucket_name, field, value, end_value=None):
    client = riak.RiakClient(host=settings['HOST'], port=settings['PORT'], transport_class=settings['TRANSPORT_CLASS'])
    pp = pprint.PrettyPrinter(depth=2, indent=4)

    start_time = time.time()

    if end_value:
        print 'using range values'
        results = client.index(bucket_name, field, value, end_value).run()
    else:
        results = client.index(bucket_name, field, value, end_value).run()

    end_time = time.time()
    elapsed_time  = end_time - start_time

    print '\033[0;33mFound %s document(s)...\n\033[0m' % len(results)
    print '\033[0;33mDisplaying top 5 results...\n\033[0m'

    for i,link in enumerate( results[:5] ):
        print '#%s:' % (i + 1)
        pp.pprint( link.get().get_data() )
        print 

    print '\033[0;34mQuery time: %0.2f seconds\n\033[0m' % elapsed_time


if __name__ == '__main__':
    if len( sys.argv ) < 4:
        print '\033[0;31mthree arguments required\033[0m'
        sys.exit(1)

    try:
        query(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    except IndexError:
        query(sys.argv[1], sys.argv[2], sys.argv[3])

