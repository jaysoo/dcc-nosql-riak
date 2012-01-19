#!/usr/bin/env python
import pprint, time, sys
import riak
from settings import settings

def mapreduce(bucket_name, field_name):
    client = riak.RiakClient(host=settings['HOST'], port=settings['PORT'], transport_class=settings['TRANSPORT_CLASS'])
    pp = pprint.PrettyPrinter(depth=2, indent=4)
    start_time = time.time()

    query = client.add(bucket_name)

    # Find sample types
    query.map('''
    function(value, key_data, arg) {
        var data = Riak.mapValuesJson(value)[0],
            value = data.%s;

        return value 
            ?  [value]
            : [];
    }
    ''' % field_name)

    # Sort by sample_id
    query.reduce('''
    function(values, arg) {
        var o = {}, 
            i,
            l = values.length, 
            r = [];

        for (i = 0; i < l; i += 1) {
            o[values[i]] = values[i];
        }

        for (i in o) {
            r.push(o[i]);
        }

        return r;
    }
    ''')

    results = query.run()

    end_time = time.time()
    elapsed_time  = end_time - start_time

    pp.pprint(results)
    print

    print '\033[0;34mQuery time: %0.2f seconds\n\033[0m' % elapsed_time


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print '\033[0;31mBucket and field names required\n\033[0m'
        sys.exit(1)

    bucket_name = sys.argv[1]
    field_name = sys.argv[2]

    print '\033[0;33mSearching all values for field \"%s\" in bucket \"%s\"...\n\033[0m' % (bucket_name, field_name)

    mapreduce(bucket_name, field_name)
