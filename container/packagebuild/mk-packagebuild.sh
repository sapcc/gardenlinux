#!/bin/bash

thisDir="$(dirname "$(readlink -f "$BASH_SOURCE")")"

GARDENLINUX_BUILD_CRE=${1}
VERSION=${2}
VERSION_DATE=${3}
VERSION_FULL=${4}

USAGE="Usage: $0 <gardenlinux-build-cre> <version> <version-date> <major.minor> - Aborting"

[ -z "$GARDENLINUX_BUILD_CRE" ] && echo "$USAGE" && exit 1
[ -z "$VERSION" ] && echo "$USAGE" && exit 1
[ -z "$VERSION_DATE" ] && echo "$USAGE" && exit 1

cat << EOF > ${thisDir}/sources.list
deb http://snapshot.debian.org/archive/debian/${VERSION_DATE}T000000Z bookworm main
deb http://snapshot.debian.org/archive/debian-security/${VERSION_DATE}T000000Z bookworm-security main
deb http://snapshot.debian.org/archive/debian/${VERSION_DATE}T000000Z bookworm-updates main
EOF

${GARDENLINUX_BUILD_CRE} build \
    --build-arg VERSION_DATE=${VERSION_DATE} \
    --build-arg TARGET_ARCH="amd64" \
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
    -t gardenlinux/packagebuild-go:${VERSION} \
    -t gardenlinux/packagebuild-go:${VERSION_FULL} \
    -t gardenlinux/packagebuild-go:${VERSION_DATE} \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild-go:${VERSION} \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild-go:${VERSION_FULL} \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild-go:${VERSION_DATE} \
    -f ${thisDir}/Dockerfile.go.cross \
    ${thisDir} 

${GARDENLINUX_BUILD_CRE} build \
    --build-arg VERSION_DATE=${VERSION_DATE} \
    --build-arg VERSION_FULL=${VERSION_FULL} \
    --build-arg TARGET_ARCH="amd64" \
    -t gardenlinux/packagebuild-lkm:${VERSION} \
    -t gardenlinux/packagebuild-lkm:${VERSION_FULL} \
    -t gardenlinux/packagebuild-lkm:${VERSION_DATE} \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild-lkm:${VERSION} \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild-lkm:${VERSION_FULL} \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild-lkm:${VERSION_DATE} \
    -f ${thisDir}/Dockerfile.lkm.cross \
    ${thisDir} 


if [ -v GHCR_UPLOAD ];then
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild:${VERSION}"
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild:${VERSION_FULL}"
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild:${VERSION_DATE}"

    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild-go:${VERSION}"
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild-go:${VERSION_FULL}"
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild-go:${VERSION_DATE}"

    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild-lkm:${VERSION}"
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild-lkm:${VERSION_FULL}"
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild-lkm:${VERSION_DATE}"
fi