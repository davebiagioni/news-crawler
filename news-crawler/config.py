import os
import logging as log

def here():
  return os.path.dirname(os.path.realpath(__file__))

def root():
  return os.path.abspath(os.path.join(here(), '..'))

def rss_dir():
  return os.path.abspath(os.path.join(root(), 'rss'))

def feed_dir():
  d = os.path.join(root(), os.path.join('data', 'feeds'))
  if not os.path.exists(d):
    os.makedirs(d)
  return d

def default_db():
  d = os.path.join(root, 'data')
  if not os.path.exists(d):
    os.makedirs(d)
  return d
  
def logging():
  logfile = os.path.join(here(), 'log.txt')
  log.basicConfig(
    filename='log.txt',
    filemode='a', 
    format='%(asctime)s | %(levelname)-5.5s | %(message)s', 
    level=log.INFO
  )
  return log
