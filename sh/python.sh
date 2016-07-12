#!/usr/bin/env bash

cd /home/vagrant
sudo apt-get install libssl-dev openssl -y
wget https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tgz
tar xzvf Python-3.5.0.tgz && rm Python-3.5.0.tgz
cd Python-3.5.0
./configure
make
sudo make install
cd ..
rm -rf Python-3.5.0