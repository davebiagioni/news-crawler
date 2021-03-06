#!/usr/bin/env python

import requests
import json
import os
import glob
import multiprocessing
import argparse
import sys
import sql
import config
import normalize
from downloadRSS import today

ALCHEMY_URL = 'https://gateway-a.watsonplatform.net/calls/url/URLGetCombinedData'
log = config.logging()

def write(data, filename):
  with open(filename, 'w') as f:
    json.dump(data, f)
  log.info('Wrote {}'.format(filename))

def enrich_url(args):
  target_url, apikey = args[:2]
  data = {
    "outputMode": 'json',
    "extract": 'doc-sentiment,entity,keyword,relation,doc-emotion,taxonomy,title,concepts',
    "emotion": 1,
    "showSourceText": 1,
    "apikey": apikey,
    "url": target_url
  }
  return requests.post(ALCHEMY_URL, data=data, timeout=args[8])

def process_feed(args):

  try:

    # Attempt to enrich the URL.
    res = enrich_url(args)

    # Check for any error code.
    if not (res.status_code >= 200 and res.status_code < 300):
      log.error('Error enriching {}'.format(args[0]))
      log.error(res.json())
      log.error('Failed on HTTP code {}: {}'.format(res.status_code, args[1]))
      return 'error'

    # Normalize the document to set correct field types.
    res = normalize.main(res.json())

    # Add the label field.
    res['label'] = args[7]

    # Write to file.
    write(res, args[2])

    # Insert to elasticsearch.
    #_ = es.insert(args[5], args[3], args[4], res, args[2])

    # Add to dedup database.
    sql.insert(args[6], today(), args[0])
    
    return res

  except:

    return False

def get_feeds(feed_dir):
  return glob.glob(os.path.join(feed_dir, '*.json'))

def create_outdir(outdir):
  if not outdir:
    outdir = os.path.join(config.here(), os.path.join('..', os.path.join(
      'data', os.path.join('articles', today()))))
    outdir = os.path.abspath(outdir)
  if not os.path.exists(outdir):
    os.makedirs(outdir)
    log.info('Created {}'.format(outdir))
  return outdir

def get_basenames(feed, num, outdir):
  basename = os.path.basename(feed).split('.json')[0]
  basenames = [os.path.join(outdir, '{}_{}.json'.format(basename, ix)) for ix in range(num)]
  return basenames

def get_label_from_path(feed):
  filename = os.path.basename(feed)
  return filename.split('-')[0]

def main(apikey, feed_dir, outdir, db_file, dry_run, timeout):

  feeds = get_feeds(feed_dir)
  outdir = create_outdir(outdir)
  pool = multiprocessing.Pool()

  if not os.path.exists(db_file):
    sql.create(db_file)

  for feed in feeds:

    try:

      # Get class from feed name
      label = get_label_from_path(feed)

      # Read feed files.
      with open(feed, 'r') as f:
        feed_data = json.load(f)
      
      # Get urls from feed files.
      urls = [x['link'] for x in feed_data['entries']]
      log.info('Found {} urls for feed {}'.format(len(urls), feed))

      # Deduplicate
      log.info('Deduplicating urls...')
      urls = sql.deduplicate(urls, db_file)
      log.info('Number of novel urls: {}'.format(len(urls)))

      # If in dry run mode or there are no novel urls, don't do anything else.
      if  dry_run or len(urls) == 0:
        continue

      # Get base filenames from urls.
      outnames = get_basenames(feed, len(urls), outdir)
      args = zip(urls, [apikey]*len(urls), outnames, [index]*len(urls),
        [doc_type]*len(urls), [es_host]*len(urls), [db_file]*len(urls),
        [label]*len(urls), [timeout]*len(urls))

      # Multiprocess feeds.
      _ = pool.map(process_feed, args)
      
    except:
    
      log.error('Error processing feed {}'.format(feed))
      log.error(sys.exc_info()[0])

  pool.close()
  pool.join()


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Ingest urls from in feeds')
  parser.add_argument('apikey', type=str, help='Alchemy apikey')
  parser.add_argument('--db-file', type=str, help='SQL db file used for storing previously crawled URLs')
  parser.add_argument('--feed-dir', type=str, help='Directory to read feeds from.  Defaults to "../data/feeds/<today>"')
  parser.add_argument('--out-dir', type=str, help='Directory for output. Defaults to "../data/articles/<today>')
  parser.add_argument('--dry-run', help='Run script without calling Alchemy.', action='store_true')
  parser.add_argument('--timeout', type=float, help='Timeout for requests in seconds', default=30.0)
  args = parser.parse_args()

  if not args.db_file: args.db_file = sql.get_default_db()
  if not args.feed_dir: args.feed_dir = os.path.join(config.feed_dir(), today())
  if not args.dry_run: args.dry_run = False

  log.info(args)
  
  _ = main(args.apikey, args.feed_dir, args.out_dir, args.db_file, args.dry_run, args.timeout)
