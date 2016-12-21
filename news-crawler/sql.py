'''
  Module to create a simple sql database for recording crawled urls.
  This is used to avoid outright duplication of enriched articles.
'''

import sqlite3
import argparse
import os
import logging
import sys
import config

log = config.logging()

def get_default_db():
  return os.path.join(config.here(), os.path.join('..', os.path.join('data', 'urls.db')))

def connect(db_file):
  return sqlite3.connect(db_file)

def insert(db_file, date, urls):
  if type(urls) is not list:
    urls = [urls]
  urls = [str(x) for x in urls]
  conn = connect(db_file)
  c = conn.cursor()
  for url in urls:
    c.execute('INSERT INTO urls VALUES (?,?)', (date, url))
    conn.commit()
  conn.close()
  log.info('Inserted {}'.format(url))
  return True

def url_exists(db_file, url, c=None):
  if not c:
    new_c = True
    conn = connect(db_file)
    c = conn.cursor()
  else:
    new_c = False
  c.execute('SELECT * FROM urls WHERE url=?;', (url,))
  if c.fetchone():
    result = True
  else:
    result = False
  if new_c:
    conn.close()
  return result

def deduplicate(urls, db_file):
  if type(urls) is str:
    urls = [urls]
  if not os.path.exists(db_file):
    log.error('db {} does not exist, exiting'.format(db_file))
    return False
  conn = connect(db_file)
  c = conn.cursor()
  new_urls = []
  for url in urls:
    if not url_exists(db_file, url, c):
      new_urls.append(url)
  conn.close()
  return new_urls

def create(db_file):
  conn = connect(db_file)
  c = conn.cursor()
  c.execute('''CREATE TABLE urls (date text, url text )''')
  log.info('Created table "urls" in {}'.format(db_file))
  conn.close()

def main(db_file):
  dirname = os.path.dirname(db_file)
  if not os.path.exists(dirname):
    _ = os.makedirs(dirname)
  if os.path.exists(db_file):
    log.warning('db {} already exists, exiting'.format(db_file))
    return False
  create(db_file)
  return True

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Create a simple SQL db for deduplication')
  parser.add_argument('--db-file', type=str, help='Name of the db file')
  args = parser.parse_args()

  if not args.db_file:
    args.db_file = get_default_db()

  _ = main(args.db_file)
