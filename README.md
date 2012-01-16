Wiki: https://wiki.oicr.on.ca/display/biomart/NoSQL+Databases+for+DCC

Requirements
------------

* [Riak](http://wiki.basho.com/Installation.html)
* [Node.js](http://nodejs.org/)
* [npm](http://npmjs.org/)
* npm modules: riak-js, seq, undercore

Loading data
------------

Run the load\_data.js script with the name of the TSV file to load:

    node load_data.js /path/to/file.tsv


Searching data
--------------

Run search.js with the name of the bucket and the search term(s).

    node search.js snp "chromosome_strand:1"

