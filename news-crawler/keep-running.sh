#!/bin/bash
while true; do
  ./$1
  echo "sleeping for ${2} seconds..."
  sleep $2
done

