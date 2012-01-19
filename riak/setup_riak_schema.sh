#!/bin/sh

search-cmd set-schema sample $PWD/schema/naive.erl
search-cmd install sample

search-cmd set-schema snp $PWD/schema/naive.erl
search-cmd install snp

