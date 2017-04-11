#!/bin/bash

LOG_FILE=log.txt
cd /home/ubuntu/news-crawler/news-crawler/
source activate default
python -W ignore downloadRSS.py 
python -W ignore crawl.py `cat key.txt` --index news --doc-type docs 
