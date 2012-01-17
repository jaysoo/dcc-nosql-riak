var riak = require('riak-js'),
    _ = require('underscore'),
    settings = require('./settings').SETTINGS;

if (process.argv.length < 4)
    console.log('\033[0;31m' + process.argv[1] + ' requires two arguments\033[0m'), process.exit(1);

var db = riak.getClient({ host: settings.RIAK_HOST, port: settings.RIAK_PORT }),
    bucket = process.argv[2],
    term = process.argv[3],
    start = new Date().getTime(),
    end = null;

db.search(bucket, term, function(error, data, meta) {
    end = new Date().getTime();
    console.log('Found: ' + data.numFound);
    console.log('\033[0;33m\nTop 10 results:\033[0m\n');
    var top_10 = data.docs.slice(0, 10);
    console.log( 
        _.map(top_10, function(doc, i) {
            return '    ' + (i + 1) + ': ' + JSON.stringify(doc.fields);
        }).join('\n')
    );
    console.log('\n\033[0;33mTime: ' + ((end - start) / 1000).toFixed(2) + ' seconds\033[0m');
});

