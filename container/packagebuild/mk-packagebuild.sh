#!/bin/bash

thisDir="$(dirname "$(readlink -f "$BASH_SOURCE")")"

GARDENLINUX_BUILD_CRE=${1}
VERSION=${2}
VERSION_DATE=${3}
VERSION_FULL=${4}
DEBIAN_SUITE=${5}

USAGE="Usage: $0 <gardenlinux-build-cre> <version> <version-date> <major.minor> <debian suite>- Aborting"

[ -z "$GARDENLINUX_BUILD_CRE" ] && echo "$USAGE" && exit 1
[ -z "$VERSION" ] && echo "$USAGE" && exit 1
[ -z "$VERSION_DATE" ] && echo "$USAGE" && exit 1
[ -z "$DEBIAN_SUITE" ] && echo "$USAGE" && exit 1

cat << EOF > ${thisDir}/sources.list.frozen
deb http://snapshot.debian.org/archive/debian/${VERSION_DATE}T000000Z ${DEBIAN_SUITE} main
deb http://snapshot.debian.org/archive/debian-security/${VERSION_DATE}T000000Z ${DEBIAN_SUITE}-security main
deb http://snapshot.debian.org/archive/debian/${VERSION_DATE}T000000Z ${DEBIAN_SUITE}-updates main
deb http://repo.gardenlinux.io/gardenlinux ${VERSION_FULL} main
EOF

cat << EOF > ${thisDir}/sources.list.current
deb http://deb.debian.org/debian ${DEBIAN_SUITE} main
deb http://deb.debian.org/debian-security ${DEBIAN_SUITE}-security main
deb http://deb.debian.org/debian ${DEBIAN_SUITE}-updates main
deb http://repo.gardenlinux.io/gardenlinux ${VERSION_FULL} main
EOF


${GARDENLINUX_BUILD_CRE} build \
    --build-arg VERSION_DATE=${VERSION_DATE} \
    --build-arg TARGET_ARCH="amd64" \
    --build-arg DEBIAN_SUITE="${DEBIAN_SUITE}" \
    -t gardenlinux/packagebuild:${VERSION} \
    -t gardenlinux/packagebuild:${VERSION_FULL} \
    -t gardenlinux/packagebuild:${VERSION_DATE} \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild:${VERSION} \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild:${VERSION_FULL} \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild:${VERSION_DATE} \
    -f ${thisDir}/Dockerfile.cross \
    ${thisDir} 

${GARDENLINUX_BUILD_CRE} build \
    --build-arg VERSION_DATE=${VERSION_DATE} \
    --build-arg TARGET_ARCH="amd64" \
    --build-arg DEBIAN_SUITE="${DEBIAN_SUITE}" \
    -t gardenlinux/packagebuild-lkm:${VERSION} \
    -t gardenlinux/packagebuild-lkm:${VERSION_FULL} \
    -t gardenlinux/packagebuild-lkm:${VERSION_DATE} \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild-lkm:${VERSION} \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild-lkm:${VERSION_FULL} \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild-lkm:${VERSION_DATE} \
    -f ${thisDir}/Dockerfile.lkm.cross \
    ${thisDir} 

# Uploading the images in this script allows to easily upload them also manually if required. 
# Requirements: GHCR_UPLOAD variable is set, and user is logged in to ghcr
if [ -v GHCR_UPLOAD ];then
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild:${VERSION}"
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild:${VERSION_FULL}"
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild:${VERSION_DATE}"

    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild-lkm:${VERSION}"
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild-lkm:${VERSION_FULL}"
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild-lkm:${VERSION_DATE}"
fi