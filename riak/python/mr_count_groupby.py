#!/usr/bin/env python
import pprint, time
import riak
from settings import settings

def mapreduce():
    client = riak.RiakClient(host=settings['HOST'], port=settings['PORT'], transport_class=settings['TRANSPORT_CLASS'])
    pp = pprint.PrettyPrinter(depth=2, indent=4)
    start_time = time.time()

    query = client.add('sample')

    query.map('''
    function(value, keyData, arg) {
        var data = Riak.mapValuesJson(value)[0],
            count = {},
            key = data.gender || 'not_specified';

        count[key] = {};
        count[key][data.sample_id] = 1;
        return [count];
    }
    ''')

    # Sort by sample_id
    query.reduce('''
    function(values, arg) {
        return [ values.reduce(function(acc, item) {
            for (var gender in item) {
                if (!item.hasOwnProperty(gender))
                    continue;

                var samples = item[gender];

                for (var sample in samples) {
                    if (!samples.hasOwnProperty(sample))
                        continue;

                    if (gender in acc) 
                        acc[gender] += item[gender][sample];
                    else 
                        acc[gender] = item[gender][sample];
                }
            }
            return acc;
        }, {})];
    }
    ''')

    results = query.run()

    end_time = time.time()
    elapsed_time  = end_time - start_time

    if not results:
        print '\033[0;34mNo results found\n\033[0m'
    else:
        print '\033[0;33mDisplaying count result...\n\033[0m'
        pp.pprint(results[0])
        print

    print '\033[0;34mQuery time: %0.2f seconds\n\033[0m' % elapsed_time


if __name__ == '__main__':
    print '\033[0;33mFind number of samples grouped by gender\n\033[0m'
    mapreduce()
