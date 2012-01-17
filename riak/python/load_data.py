#!/usr/bin/env python
import sys, time, re, json
import riak
from settings import settings

_slugify_strip_re = re.compile(r'[^a-zA-Z0-9_]')

def populate_bucket(filename, bucket_name, skip_first, header):
    '''
    Opens a file and loads it into a Riak bucket

    Returns the total number of documents stored
    '''

    print '\033[0;33mLoading data into "%s" bucket...\n\033[0m' %  bucket_name

    client = riak.RiakClient(host=settings['HOST'], port=settings['PORT'], transport_class=settings['TRANSPORT_CLASS'])
    bucket = client.bucket(bucket_name)
    total = 0

    for i,line in enumerate( open(filename) ):

        # Might need to skip first line
        if i == 0 and skip_first:
            continue

        # Replace all \N values with None
        values = [ None if v == '\\N' else v for v in line.split('\t') ]
        data = dict( zip([ str(h['name']) for h in header ], values) )

        _store_data(client, bucket, str(i), data)

        total = i + 1

    print '\033[0;33m... Loaded %s documents\n\033[0m' % total
    

    return total

def _generate_bucket_name(filename):
    ''' 
    Grab the file name from a path and remove the extension
    '''
    return filename.split('/')[-1].split('.')[0]

def _store_data(client, bucket, id, data):
    obj = riak.RiakObject(client, bucket, id)
    obj.set_data(data)
    obj.set_content_type('application/json')
    obj._encode_data = True

    # Set indexes
    for k,v in data.items():
        obj.add_index('%s_bin' % k, v)

    # Try to optimize for write speed
    obj.store(w=0, dw=0, return_body=False)

if __name__ == '__main__':
    if len( sys.argv ) < 2:
        print '\033[0;31mschema file argument required\033[0m'
        sys.exit(1)

    # Read in schema
    schema_file = sys.argv[1]

    with open(schema_file) as f:
        schema = json.loads( f.read() )

    total = 0
    start_time = time.time()

    for s in schema:
        total += populate_bucket(s['file'], s['bucket'], s['skip_first'], s['columns'])

    end_time = time.time()

    total_time = (end_time - start_time)

    print '\033[0;33m\n... Loading successful!\033[0m'

    # Print stats
    print '''\033[0;34mPrinting stats:
    Total documents: %s
    Time elapsed: %0.2f seconds
    Writes per second: %0.2f 
    \033[0m''' % ( total, total_time, total / total_time )



