#!/bin/sh
# Entrypoint of Garden Linux installation via onie
# Based on https://github.com/nkraetzschmar/gardenlinux/blob/eb45ee05f23e0b359535d031ea5740b916def38c/garden_linux_nos_installer.sh

set -exufo pipefail

ROOT_PART_LABEL="ROOT"


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


echo "### Creating partition layout"

blk_dev=$(blkid | grep -F 'LABEL="ONIE-BOOT"' | head -n 1 | awk '{ print $1 }' |  sed 's/[1-9][0-9]*:.*$//' | sed 's/\([0-9]\)\(p\)/\1/')

if [ ! -b "$blk_dev" ]; then
    echo "### Aborting. invalid blk_dev=$blk_dev"
    exit 1
fi

echo "... using same blk device as ONIE-BOOT: $blk_dev"
last_part_num="$(sgdisk -p $blk_dev | tail -n 1 | awk '{ print $1 }')"
part_num="$(( $last_part_num + 1 ))"
sgdisk --largest-new="$part_num" --change-name="$part_num:$ROOT_PART_LABEL" "$blk_dev"
partprobe

blk_suffix=""
(echo "$blk_dev" | grep -q mmcblk || echo "$blk_dev" | grep -q nvme) && blk_suffix="p"

part_dev="$blk_dev$blk_suffix$part_num"

echo "### Creating filesystems"
mkfs.ext4 -F -L "$ROOT_PART_LABEL" "$part_dev"
mount -t ext4 -o defaults,rw "$part_dev" "$tmp_dir"

echo "### Self extracting garden linux rootfs"
sed '1,/^# --- EXIT MARKER 8c5daf21-e9d9-4a7f-b4b9-fd653d8c701b ---$/d' "$0" | base64 -d | xz -d | tar -x -C "$tmp_dir"


echo "### Installing and Configuring GRUB "
grub-install --boot-directory="$tmp_dir" --recheck "$blk_dev"

. /mnt/onie-boot/onie/grub/grub-variables



echo "### Cleaning up temp installation dir"
umount $tmp_dir
rm -rf $tmp_dir


echo "### "




onie-nos-mode -s

echo "### Success"

# --- EXIT MARKER 8c5daf21-e9d9-4a7f-b4b9-fd653d8c701b ---
