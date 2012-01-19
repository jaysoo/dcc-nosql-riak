#!/usr/bin/env python
import pprint, time
import riak
from settings import settings

def mapreduce():
    client = riak.RiakClient(host=settings['HOST'], port=settings['PORT'], transport_class=settings['TRANSPORT_CLASS'])
    pp = pprint.PrettyPrinter(depth=2, indent=4)
    start_time = time.time()

    query = client.add('sample')

    # Find sample types
    query.map('''
    function(value, key_data, arg) {
        var data = Riak.mapValuesJson(value)[0],
        grouped = {};
        if (data.sample_type) {
            grouped[data.sample_type] = 1;
        } else {
            grouped.unspecified = 1;
        }
        return [grouped];
    }
    ''')

    # Sort by sample_id
    query.reduce('''
    function(values, arg) {
        return [values.reduce(function(acc, value) {
            for (var group in value) {
                if(group in acc)
                    acc[group] += value[group];
                else
                    acc[group] = value[group];
            }
            return acc;
        }, {})];
    }
    ''')

    results = query.run()

    end_time = time.time()
    elapsed_time  = end_time - start_time

    print '\033[0;33mDisplaying results...\n\033[0m'
    pp.pprint(results[0])
    print

    print '\033[0;34mQuery time: %0.2f seconds\n\033[0m' % elapsed_time


if __name__ == '__main__':
    print '\033[0;33mFind number of samples grouped by sample type\n\033[0m'
    mapreduce()
