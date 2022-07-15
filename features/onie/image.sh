#!/bin/sh

# Creates a self extracting image

set -Eexuo pipefail

thisScript=$(realpath "$0")
wd=$(dirname "$thisScript")

rootfs="$1"
targetBase="$2"

output_file="${targetbase}.bin"
tmp_dir=$(mktemp --directory)
rootfs_tar="${tmp_dir}/rootfs.tar"


cp "$wd/nos-installer.sh" "$output_file"
tar -cf "$rootfs_tar" "$rootfs"

cat "$rootfs_tar" >> "$output_file" 


rm -rf $tmp_dir


