#!/bin/bash
curl -XPUT localhost:9200/news
curl -XPUT -H "Content-Type: application/json" -d @mapping.json localhost:9200/news/_mapping/docs
echo
