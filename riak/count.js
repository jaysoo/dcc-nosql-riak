var riak = require('riak-js'),
    _ = require('underscore'),
    csv = require('csv'),
    fs = require('fs'),
    // seq = require('seq'),
    num_cpus = require('os').cpus().length,

    settings = require('./settings').SETTINGS;

if (process.argv.length < 3)
    console.log('\033[0;31m' + process.argv[1] + ' requires a file argument\033[0m'), process.exit(1);

var db = riak.getClient({ host: settings.RIAK_HOST, port: settings.RIAK_PORT }),
    bucket = process.argv[2];

db.add(bucket).map(snp_ones).reduce(count_snps).run(function(error, data, meta) {
    console.log(data[0]);
});

function snp_ones(value) {
    try {
        return [1]; 
    } catch (error) { 
        return [];
    }
}

function count_snps(values) {
    return [ values.reduce(function(total, value) {
            if (isNaN(parseInt(value))) {
                return total + 1;
            } else {
                return total + value;
            }
        }, 0) ];
}
