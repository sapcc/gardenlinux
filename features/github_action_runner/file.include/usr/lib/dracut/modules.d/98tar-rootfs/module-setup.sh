#!/bin/bash

check() {
	require_binaries tar xz || return 1
	return 255
}

depends() {
	echo "dracut-systemd"
}

install() {
	inst_multiple tar xz

	inst_simple "$moddir/sysroot.mount" "$systemdsystemunitdir/sysroot.mount"
	inst_simple "$moddir/tar-rootfs.service" "$systemdsystemunitdir/tar-rootfs.service"

	systemctl -q --root "$initdir" add-requires initrd-root-fs.target sysroot.mount
	systemctl -q --root "$initdir" add-requires initrd-root-fs.target tar-rootfs.service
}
