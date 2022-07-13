#!/bin/sh

# Entrypoint of Garden Linux installation via onie


echo "### Verifying image checksum"
# TODO: implement verify checksum
echo "    Skipped (not implemented)"


echo "### Creating temp installation dir"
entry_wd=$(pwd)
tmp_dir=$(mktemp -d)
mount -t tmpfs tmpfs-installer $tmp_dir || exit 1


echo "### Preparing Garden Linux image archive"
cd $tmp_dir
sed -e '1,/^exit_marker$/d' $archive_path | tar xf - || exit 1
cd $entry_wd


echo "### Checking Requirements"

if [ ! -d "/sys/firmware/efi/efivars" ]; then
    echo "### Aborting. Only UEFI boot is implemented"
    exit 1
fi



echo "### Creating Partition"




echo "### Cleaning up temp installation dir"
umount $tmp_dir
rm -rf $tmp_dir

echo "### Success"
exit_marker
