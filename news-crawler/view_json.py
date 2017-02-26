#!/usr/bin/python

import pprint
import json
import argparse
import os

def main(filename):
  pp = pprint.PrettyPrinter(indent=2)
  if not os.path.exists(filename):
    print('Not found: {}'.format(filename))
  with open(filename, 'r') as f:
    pp.pprint(json.load(f))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Pretty print a JSON file')
  parser.add_argument('filename', type=str, help='JSON file.')
  args = parser.parse_args()

  _ = main(args.filename)
