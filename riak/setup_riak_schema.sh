#!/bin/sh

search-cmd set-schema sample $PWD/schema/sample.erl
search-cmd install sample

search-cmd set-schema snp $PWD/schema/snp.erl
search-cmd install snp

