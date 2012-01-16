/*
 * Parses a TSV file and loads the data into Riak. The first line of the TSV file must be the header.
 *
 * You also need to set the Riak host and port as RIAK_HOST and RIAK_PORT environment variables respectively.
 *
 * Usage:
 *   node load_data.js [file]
 *
 */

// Imports
var riak = require('riak-js'),
    _ = require('underscore'),
    csv = require('csv'),
    fs = require('fs'),
    // seq = require('seq'),
    num_cpus = require('os').cpus().length,

    settings = require('./settings').SETTINGS;

if (process.argv.length < 3)
    console.log('\033[0;31m' + process.argv[1] + ' requires a file argument\033[0m'), process.exit(1);

var db = riak.getClient({ host: settings.RIAK_HOST, port: settings.RIAK_PORT })

// Helper vars and functions
var total = 0 /* counter for total rows loaded */,

    processed = 0,

    file = process.argv[2],

    // Use the file name (minus extension) as Riak bucket name
    bucket = file.split('.')[0].split('/').pop(),

    // array of headers parsed
    headers = null,

    // For timing total run time
    timer = { 
        start: new Date().getTime(), 
        end: null
    },

    remaining_chunk = '';

console.log('\033[0;33mLoading data into "' + bucket + '" bucket...\n\033[0m');

// If using relative path, prepend working dir 
if ( !(/^\//).test(file) )
    file = __dirname + '/' + file;

db.updateProps(bucket, settings.RIAK_BUCKET_PROPS, function(error) {
    if (error)
        console.log(error), process.exit(1);

    var stream = fs
        .createReadStream(file, { 
            bufferSize: 64 * 1024,
            flags: 'r'
        })
        .addListener('data', function(chunk) {
            var lines = ( remaining_chunk + chunk ).split('\n');

            remaining_chunk = lines.pop();

            for (var i = 0, line; line = lines[i]; i++)
                process_line(line);
        })
        .addListener('close', function() {
            remaining_chunk && process_line(remaining_chunk);
        });
});

// Convert \N to null
function map_nulls(data) {
    return _.map(data, function(value) {
        return value == '\\N'
            ? null
            : value;
    });
}

function process_line(line) {
    line = map_nulls( line.split('\t') );

    if (!total++) {
        headers = line;
    } else {
        var json_data = {};

        processed++;

        // populate keys and values
        for (var i = 0; i < line.length; i++)
            json_data[headers[i]] = line[i];

        db.save(bucket, line[0], json_data, { w: 0, dw: 0, returnbody: false }, function(error) {
            if (error != null)
                console.log(error);

            if (--processed === 0) 
                print_stats();
        });
    }
}

function print_stats() {
    console.log('\033[0;33m\n...Loaded ' + total + ' rows\033[0m');

    timer.end = new Date().getTime();

    console.log('\033[0;34m\nStats:');

    var total_time = ( timer.end - timer.start ) / 1000;
    
    console.log(
        '    Total time = ' + total_time.toFixed(2) + ' seconds\n' +
        '    Inserts = ' + total + '\n' +
        '    Operations per second = ' + ( total / total_time ).toFixed(2) + '\n\033[0m'
    );
}
