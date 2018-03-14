#!/bin/bash

while getopts hqv: opt
do
  case $opt in
    h) echo "$0 -h -q -v'arg'" >&2; exit 0 ;;
    q) echo >&2 $opt ;;
    v) echo >&2 $opt $OPTARG ;;
    \?) echo >&2 '*error*' ;exit 1;;
    :) echo >&2 "arg not found for '$OPTARG'" ;exit 1;;
  esac
done
shift $((OPTIND-1))

echo $'---\nRemaining args after getopts'
echo $'---\n'"$*"

