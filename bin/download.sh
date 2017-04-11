#!/bin/bash
DATADIR=$HOME/gitrepos/news-crawler/data
mkdir -p $DATADIR
rsync -avP ubuntu@ec2-54-165-0-32.compute-1.amazonaws.com:/home/ubuntu/news-crawler/data/* $DATADIR/.
