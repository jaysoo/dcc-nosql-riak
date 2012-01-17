#!/usr/bin/env python
import sys, time
import riak
from settings import settings

def populate_bucket(filename, bucket_name=None):
    '''
    Opens a file and loads it into a Riak bucket

    Returns the total number of documents stored
    '''
    if not bucket_name:
        bucket_name = _generate_bucket_name(filename)

    print '\033[0;32mLoading data into "%s" bucket...\n\033[0m' %  bucket_name

    client = riak.RiakClient(host=settings['HOST'], port=settings['PORT'], transport_class=settings['TRANSPORT_CLASS'])
    bucket = client.bucket(bucket_name)
    total = 0
    header = None

    for i,line in enumerate( open(filename) ):

        # First line is the header
        if i == 0:
            header = [ h.strip().replace(' ', '_') for h in line.split('\t') ]
            continue

        values = line.split('\t')
        data = _generate_document_data(header, values) 

        _store_data(client, bucket, str(i), data)

        total = i + 1

    print '\033[0;32m\n... Loading successful!\033[0m'

    return total

def _generate_bucket_name(filename):
    ''' 
    Grab the file name from a path and remove the extension
    '''
    return filename.split('/')[-1].split('.')[0]

def _generate_document_data(header, values):
    '''
    Generates document hash data given a list of the header and values
    '''
    document = {}

    for i,value in enumerate(values):
        document[ header[i] ] = value

    return document

def _store_data(client, bucket, id, data):
    new_doc = riak.RiakObject(client, bucket, id)
    new_doc.set_data(data)
    new_doc.set_content_type('application/json')
    new_doc._encode_data = True
    new_doc.store()

if __name__ == '__main__':
    if len( sys.argv ) < 2:
        print '\033[0;31mfile argument required\033[0m'
        sys.exit(1)

    start_time = time.time()

    try:
        total = populate_bucket(sys.argv[1], sys.argv[2])
    except IndexError:
        total = populate_bucket(sys.argv[1])

    end_time = time.time()

    total_time = (end_time - start_time)

    # Print stats
    print '''\033[0;33mPrinting stats:
    Total documents: %s
    Time elapsed: %0.2f seconds
    Writes per second: %0.2f 
    \033[0m''' % ( total, total_time, total / total_time )



