#!/usr/bin/env bash

sudo apt-get install libpq-dev
sudo apt-get install postgresql postgresql-contrib
sudo -i -u postgres

# psql
# CREATE DATABASE test_database;
# CREATE USER vagrant  WITH password 'q!w@e3r4t%';
# GRANT ALL privileges ON DATABASE test_database TO vagrant;
# \q
# exit