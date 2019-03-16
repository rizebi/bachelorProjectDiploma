#!/bin/sh

chmod 777 populateDB.py
./populateDB.py

cd ./client
chmod 777 ./run.sh
./run.sh

cd ../server
chmod 777 ./run.sh
./run.sh

cd ../admin
chmod 777 ./run.sh
./run.sh