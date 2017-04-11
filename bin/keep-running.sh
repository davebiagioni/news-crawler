#!/bin/bash
# Hacky alternative to cron job ... runs command, sleeping for a
# specified number of minutes between runs.
#
# Usage:
#  ./keep-running ./run.sh 1440

while true; do
  ./$1
  echo "sleeping for ${2} seconds..."
  sleep $2
done

