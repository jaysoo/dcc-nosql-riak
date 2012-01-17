var riak = require('riak-js'),
    _ = require('underscore'),
    settings = require('./settings').SETTINGS;

if (process.argv.length < 4)
    console.log('\033[0;31m' + process.argv[1] + ' requires two arguments\033[0m'), process.exit(1);

var db = riak.getClient({ host: settings.RIAK_HOST, port: settings.RIAK_PORT }),
    bucket = process.argv[2],
    start = new Date().getTime(),
    end = null,
    query = JSON.parse(process.argv[3]);

db.query(bucket, query, function(error, data, meta) {
    end = new Date().getTime();
    console.log(JSON.stringify(data));
    console.log('\n\033[0;33mTime: ' + ((end - start) / 1000).toFixed(2) + ' seconds\033[0m');
});

