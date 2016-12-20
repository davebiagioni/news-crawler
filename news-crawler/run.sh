#!/bin/bash

cd /home/ubuntu/news-crawler/news-crawler/
source activate default
python -W ignore downloadRSS.py
python -W ignore crawl.py --index news --doc-type docs --host http://localhost:9200 --db-file ../data/urls.db
