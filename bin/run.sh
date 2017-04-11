#!/bin/bash
# Activates the anaconda virtual env, downloads URLs for each RSS feed,
# and crawls them.

LOG_FILE=log.txt
cd /home/ubuntu/news-crawler/news-crawler/
source activate default
python -W ignore downloadRSS.py 
python -W ignore crawl.py `cat key.txt` --index news --doc-type docs 
