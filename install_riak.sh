#!/bin/sh

# Install pacakges
apt-get install build-essential checkinstall libssl-dev git-core libcrypto++-dev libssl-dev libssl0.9.8

# Install Node.js
wget http://nodejs.org/dist/v0.6.7/node-v0.6.7.tar.gz
tar zxvf node-v0.6.7.tar.gz
cd node-v0.6.7
./configure
make 
make install
curl http://npmjs.org/install.sh | sudo sh

# Install Riak
wget http://downloads.basho.com/riak/riak-1.0.2/riak_1.0.2-1_ubuntu_11_amd64.deb
dpkg -i riak_1.0.2-1_ubuntu_11_amd64.deb
