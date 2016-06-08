#!/bin/bash
filename=$1
if [[ -z $1 ]];
then
    echo "Path to cleanup list required. Use generate_cleanup_list.py to generate a list of candidates for deletion."
    echo "The cleanup list must contain a list of bucket names, one per line."
    echo "Usage: $0 [cleanup_list_file]"
    exit 1
fi
while read bucket; do
    swift download $bucket -D $bucket
    swift delete $bucket
done < $filename
