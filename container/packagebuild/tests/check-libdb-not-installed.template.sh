#!/bin/bash

FUN_UUID="__UUID__"

libdb_path=$(whereis libdb-5.3.so | cut -d':' -f2 | xargs)


if nm -g ${libdb_path} | grep -q ${FUN_UUID}; then
    echo "Success - found nodb instead of libdb"
else
    echo "Failure: Did not find libdb replacement. libdb_path: $libdb_path"
    exit 1
fi

libdb_leftovers=$(find / -type f -name "libdb*" -or -type d -name "libdb*" | grep -vF ${libdb_path})

if [ -z "$libdb_leftovers" ]; then
    echo "Success - did not find libdb leftovers"
else
    echo "Failure: found some leftovers of libdb."
    echo "libdb_leftovers: $libdb_leftovers"
    echo "libdb_path: $libdb_path"
    exit 1
fi
exit 0
