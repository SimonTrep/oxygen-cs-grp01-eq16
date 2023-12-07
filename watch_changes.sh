#!/bin/bash

sha=$(docker manifest inspect log680eq16/oxygen-cs-grp01-eq16:latest -v | grep digest | head -n1 | cut -d '"' -f 4 | cut -d ':' -f2)

while (true); do
  shanew=$(docker manifest inspect log680eq16/oxygen-cs-grp01-eq16:latest -v | grep digest | head -n1 | cut -d '"' -f 4 | cut -d ':' -f2)
  echo "$sha AND $shanew"

  if [[ "$shanew" != "$sha" ]]; then
    echo "SHA changed from $sha to $shanew"
    kubectl delete pod $(kubectl get pod | grep oxygen | awk '{print $1}')
  fi
  sha=$shanew

  sleep 10
done