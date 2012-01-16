var riak = require('riak-js'),
    settings = require('./settings').SETTINGS;

if (process.argv.length < 3)
    console.log('\033[0;31m' + process.argv[1] + ' requires a bucket argument\033[0m'), process.exit(1);

var db = riak.getClient({ host: settings.RIAK_HOST, port: settings.RIAK_PORT }),
    bucket = process.argv[2],
    start = new Date().getTime(),
    end = null;

db.add(bucket)
    .map({language: 'erlang',
        module: 'riak_kv_mapreduce',
        function: 'map_object_value'})
    .reduce({language: 'erlang',
        module: 'riak_kv_mapreduce',
        function: 'reduce_count_inputs'})
    .run(function(error, data, meta) {
        end = new Date().getTime();
        console.log('Count: ' + data[0]);
        console.log('Time: ' + ((end - start) / 1000).toFixed(2) + ' seconds');
    });

