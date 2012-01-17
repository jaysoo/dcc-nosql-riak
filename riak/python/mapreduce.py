#!/usr/bin/env python
import sys, pprint, time
import riak
from settings import settings

def mapreduce():
    client = riak.RiakClient(host=settings['HOST'], port=settings['PORT'], transport_class=settings['TRANSPORT_CLASS'])
    pp = pprint.PrettyPrinter(depth=2, indent=4)
    start_time = time.time()

    query = client.add('sample')
    query.map('''
    function(v) {
        var data = JSON.parse(v.values[0].data);
        if(data.gender == 'female') {
            return [[v.key, data]];
        }
        return [];
    }
    ''')
    query.reduce('''
    function(values) {
        return values.sort();
    }
    ''')
    results = query.run()

    end_time = time.time()
    elapsed_time  = end_time - start_time
    print '\033[0;33mDisplaying top 5 results...\n\033[0m'

    for i,data in enumerate( results[:5] ):
        print '#%s:' % (i + 1)
        pp.pprint(data)
        print 

    print '\033[0;34mFound %s document(s)...\033[0m' % len(results)
    print '\033[0;34mQuery time: %0.2f seconds\n\033[0m' % elapsed_time


if __name__ == '__main__':
    mapreduce()

