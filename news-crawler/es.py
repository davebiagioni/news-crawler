#!/usr/bin/python

import requests
import config

log = config.logging()

def insert(host, index, doc_type, data, filename):
  try:
    _ = requests.post('http://{}/{}/{}'.format(host, index, doc_type), json=data)
    log.info('Inserted to ES: {}'.format(filename))
    return True
  except:
    log.error('Failed ES insert: {}'.format(filename))
    return False
