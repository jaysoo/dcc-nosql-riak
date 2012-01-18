Wiki: https://wiki.oicr.on.ca/display/biomart/NoSQL+Databases+for+DCC

Requirements
------------

* [Riak](http://wiki.basho.com/Installation.html)
* Python modules: protobuf (install from scratch), riak

Installation
------------

Use the install_riak.sh script for setting up Riak + Node.js environment.

    curl -L https://github.com/jaysoo/dcc-nosql-riak/raw/master/install_riak.sh | sudo sh

Loading data
------------

Run the load\_data.py script with the name of the schema file:

    ./load_data.py /path/to/schema.json

