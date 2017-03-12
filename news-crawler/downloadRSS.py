#!/usr/env/bin python

from __future__ import print_function
import requests
import feedparser
import json
import glob
import argparse
import sys
import os
import re
import datetime
import time
import config
from collections import defaultdict

log = config.logging()

def summarize(data_dir):
  files = glob.glob(os.path.join(data_dir, '*.json'))
  labels = [os.path.basename(f).split('-')[0].strip() for f in files]
  counts = defaultdict(int)
  for ix, fil in enumerate(files):
    with open(fil, 'r') as f:
      d = json.load(f)
    counts[labels[ix]] += len(d['entries'])
  unique_labels = list(set(labels))
  log.info('Total files: {}'.format(len(files)))
  log.info('Entry counts:')
  for label in unique_labels:
    log.info('  {}: {}'.format(label, counts[label]))

def normalize_dict(d):
  if type(d) is feedparser.FeedParserDict:  
    d = dict(d)
  if type(d) is dict:
    for key in d.keys():
      d[key] = normalize_dict(d[key])
  elif type(d) is list:
    for ix, item in enumerate(d):
      d[ix] = normalize_dict(item)
  else:
    try:
      string = json.dumps(d, indent=2)
      return json.loads(string)
    except:
      return ''
  return d

def today():
  return datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d')

def convert_feed_to_filename(feed):
  feed = re.sub('^http://', '', feed)
  feed = re.sub('/$', '', feed)
  feed = re.sub('/', '-', feed)
  feed = '{}-{}.json'.format(feed, today())
  return feed

def parse(feed):
  try:
    return feedparser.parse(feed)
  except:
    log.error('Error parsing {}: {}'.format(feed, sys.exc_info()[0]))
    return None

def read_rss_files(rss_dir):
  feeds = []
  tags = []
  files = glob.glob(os.path.join(config.rss_dir(), 'rss*.txt'))
  for fil in files:
    with open(fil, 'r') as f:
      tmp = [x.strip() for x in f.readlines()]
      feeds.extend(tmp)
      tags.extend([fil.split('-')[-1].split('.')[0]] * len(tmp))
  return feeds, tags

def get_feed(feed, filename):

  # If feed has already been gotten today, skip it.
  if filename and os.path.exists(filename):
    log.info('Already retreived: {}'.format(filename))
    return None

  # Parse the feed
  result = parse(feed)

  # Try to write the response if you got one.
  if result and filename:
    try:
      result = normalize_dict(result)
      string = json.dumps(result, skipkeys=True, indent=2)
      with open(filename, 'w') as f:
        f.write(string)
        log.info('Wrote {}'.format(filename))
    except:
      log.error('ERROR writing {}: {}'.format(feed, sys.exc_info()[0]))
  else:
      log.error('ERROR parsing {}'.format(feed))

  return result

def main(summary=False):

  try:

    # Set default directories.
    out_dir = os.path.join(config.feed_dir(), today())
    rss_dir = config.rss_dir()

    # Create output directory if it doesn't exist.
    if not os.path.exists(out_dir):
      _ = os.makedirs(out_dir)
      log.info('Created output directory {}'.format(out_dir))

    # Log the output directory
    log.info('Set output path to {}'.format(out_dir))

    # Optionally summarize and exit.
    if summary:
      summarize(out_dir)
      return
    
    # Read RSS files.
    log.info('Reading rss files')
    feeds, tags = read_rss_files(rss_dir)

    # Convert feed names to filenames.
    log.info('Generating filenames')
    filenames = ['{}-{}'.format(t, convert_feed_to_filename(x)) for t,x in zip(tags,feeds)]
    filenames = [os.path.join(out_dir, x) for x in filenames]

    # Crawl the feeds.
    for feed, filename in zip(feeds, filenames):
      _ = get_feed(feed, filename)

  except KeyboardInterrupt:
    log.error('Aborting')
    sys.exit(1)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Crawl RSS feeds and enrich news pages')
  parser.add_argument('-s', '--summary', help='Summarize the number of RSS entries you\'ve crawled', action='store_true')
  args = parser.parse_args()

  args.summary = args.summary if args.summary else False

  try:
    _ = main(args.summary)
  except KeyboardInterrupt:
    log.error('Aborting')
    exit()

