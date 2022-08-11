#!/bin/sh
# Entrypoint of Garden Linux installation via onie
# Based on https://github.com/nkraetzschmar/gardenlinux/blob/eb45ee05f23e0b359535d031ea5740b916def38c/garden_linux_nos_installer.sh

set -exufo pipefail

ROOT_PART_LABEL="ROOT"
payload_sha1=%%IMAGE_SHA1%%
sha1=$(sed '1,/^# --- EXIT MARKER 8c5daf21-e9d9-4a7f-b4b9-fd653d8c701b ---$/d' "$0" | sha1sum | awk '{ print $1 }')


echo "### Verifying image checksum"
if [ "$sha1" != "$payload_sha1" ] ; then
    echo
    echo "ERROR: Unable to verify archive checksum"
    echo "Expected: $payload_sha1"
    echo "Found   : $sha1"
    exit 1
fi

echo "### Creating temp installation dir"
entry_wd=$(pwd)
tmp_dir=$(mktemp -d)
mount -t tmpfs tmpfs-installer $tmp_dir || exit 1

echo "### Checking Requirements"
[ "$(onie-sysinfo -c)" = "x86_64" ]
[ "$(onie-sysinfo -t)" = "gpt" ]
[ "$(onie-sysinfo -l)" = "bios" ]

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


kernel="$(cd "$mnt/boot/" && find . -name 'vmlinuz-*-amd64' | sed 's#^\./##' | tail -n 1)"
initramfs="$(cd "$mnt/boot/" && find . -name 'initrd.img-*-amd64' | sed 's#^\./##' | tail -n 1)"
[ -b "$kernel" ] && [ -b "$initramfs" ]

cat <<EOF > "$mnt/grub/grub.cfg"
$GRUB_SERIAL_COMMAND
terminal_input $GRUB_TERMINAL_INPUT
terminal_output $GRUB_TERMINAL_OUTPUT
set timeout=5
menuentry 'Garden Linux' {
        search --no-floppy --label --set=root $ROOT_PART_LABEL
        linux   /boot/$kernel $GRUB_CMDLINE_LINUX \$ONIE_EXTRA_CMDLINE_LINUX root=LABEL=ROOT rw
        initrd  /boot/$initramfs
}
EOF

/mnt/onie-boot/onie/grub.d/50_onie_grub >> "$mnt/grub/grub.cfg"


echo "### Cleaning up temp installation dir"
umount $tmp_dir
rm -rf $tmp_dir


onie-nos-mode -s

echo "### Success"
exit 0
# --- EXIT MARKER 8c5daf21-e9d9-4a7f-b4b9-fd653d8c701b ---
