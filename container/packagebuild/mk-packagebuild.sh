#!/bin/bash

set -Eeuo pipefail

thisDir="$(dirname "$(readlink -f "$BASH_SOURCE")")"

GARDENLINUX_BUILD_CRE=${1}
VERSION_DATE=${2}
VERSION_FULL=${3}
DEBIAN_SUITE=${4}
TARGET_ARCH=${5}

USAGE="Usage: $0 <gardenlinux-build-cre> <version-date> <major.minor> <debian suite> <target arch>"

[ -z "$GARDENLINUX_BUILD_CRE" ] && echo "$USAGE" && exit 1
[ -z "$VERSION_DATE" ] && echo "$USAGE" && exit 1
[ -z "$VERSION_FULL" ] && echo "$USAGE" && exit 1
[ -z "$DEBIAN_SUITE" ] && echo "$USAGE" && exit 1
[ -z "$TARGET_ARCH" ] && echo "$USAGE" && exit 1

cat << EOF > ${thisDir}/sources.list.frozen
deb http://snapshot.debian.org/archive/debian/${VERSION_DATE}T000000Z ${DEBIAN_SUITE} main
deb http://snapshot.debian.org/archive/debian-security/${VERSION_DATE}T000000Z ${DEBIAN_SUITE}-security main
deb http://snapshot.debian.org/archive/debian/${VERSION_DATE}T000000Z ${DEBIAN_SUITE}-updates main
deb [signed-by=/usr/share/keyrings/gardenlinux.gpg] http://repo.gardenlinux.io/gardenlinux ${VERSION_FULL} main
EOF

cat << EOF > ${thisDir}/sources.list.current
deb http://deb.debian.org/debian ${DEBIAN_SUITE} main
deb http://deb.debian.org/debian-security ${DEBIAN_SUITE}-security main
deb http://deb.debian.org/debian ${DEBIAN_SUITE}-updates main
deb [signed-by=/usr/share/keyrings/gardenlinux.gpg] http://repo.gardenlinux.io/gardenlinux ${VERSION_FULL} main
EOF

if [[ "$TARGET_ARCH" == "arm64" ]]; then
    BASE_IMAGE="arm64v8/debian:${DEBIAN_SUITE}-slim"
elif [[ "$TARGET_ARCH" == "amd64" ]]; then  
    BASE_IMAGE="debian:${DEBIAN_SUITE}-slim"
else
    echo "ERROR: TARGET_ARCH: '${TARGET_ARCH}' is not supported - aborting"
    exit 1
fi

# Copy Garden Linux public key
cp ${thisDir}/../../gardenlinux.asc ${thisDir}

# Create nodb as replacement for libdb
FUN_UUID=$(uuidgen | sed "s:-::g")
pushd ${thisDir}/nodb
cat nodb-template.c | sed "s#__UUID__#${FUN_UUID}#" | tee nodb.c
gcc -c -fPIC nodb.c -o nodb.o
gcc nodb.o -shared -o nodb.so
rm nodb.o
popd # nodb

# nodb.so replaces libdb-5.3.so. If the function FUN_UUID is listed in the symbols,
# then we can be sure that our library is in place.
rm -f ${thisDir}/tests/check-libdb-not-installed.real.sh
cat ${thisDir}/tests/check-libdb-not-installed.template.sh| sed "s#__UUID__#${FUN_UUID}#" | tee ${thisDir}/tests/check-libdb-not-installed.real.sh
chmod +x ${thisDir}/tests/check-libdb-not-installed.real.sh

# Latest Version uses latest debian repo (non snapshot)
${GARDENLINUX_BUILD_CRE} build \
    --build-arg BASE_IMAGE="${BASE_IMAGE}" \
    --build-arg TARGET_ARCH="${TARGET_ARCH}" \
    --platform linux/${TARGET_ARCH}  \
    -t gardenlinux/packagebuild-${TARGET_ARCH}:latest \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild:latest \
    -t docker.io/vincinator/packagebuild-${TARGET_ARCH}:latest \
    -f ${thisDir}/Dockerfile.latest \
    ${thisDir} 

# Snapshot Version uses snapshot debian repos
${GARDENLINUX_BUILD_CRE} build \
    --build-arg BASE_IMAGE="gardenlinux/packagebuild-${TARGET_ARCH}:latest" \
    --build-arg VERSION_DATE=${VERSION_DATE} \
    --platform linux/${TARGET_ARCH}  \
    -t gardenlinux/packagebuild-${TARGET_ARCH}:${VERSION_FULL} \
    -t gardenlinux/packagebuild-${TARGET_ARCH}:${VERSION_DATE} \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild:${VERSION_FULL} \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild:${VERSION_DATE} \
    -t docker.io/vincinator/packagebuild-${TARGET_ARCH}:${VERSION_DATE} \
    -t docker.io/vincinator/packagebuild-${TARGET_ARCH}:${VERSION_FULL} \
    -f ${thisDir}/Dockerfile.snapshot \
    ${thisDir} 

# Build loadable kernel module (LKM) build container based on packagebuild image
${GARDENLINUX_BUILD_CRE} build \
    --build-arg BASE_IMAGE="gardenlinux/packagebuild-${TARGET_ARCH}:${VERSION_DATE}" \
    --build-arg VERSION_DATE=${VERSION_DATE} \
    --platform linux/${TARGET_ARCH}  \
    --build-arg TARGET_ARCH="${TARGET_ARCH}" \
    -t gardenlinux/packagebuild-lkm-${TARGET_ARCH}:${VERSION_FULL} \
    -t gardenlinux/packagebuild-lkm-${TARGET_ARCH}:${VERSION_FULL} \
    -t gardenlinux/packagebuild-lkm-${TARGET_ARCH}:today \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild-lkm-${TARGET_ARCH}:${VERSION_FULL} \
    -t ghcr.io/gardenlinux/gardenlinux/packagebuild-lkm-${TARGET_ARCH}:${VERSION_DATE} \
    -f ${thisDir}/Dockerfile.lkm \
    ${thisDir} 

DOCKERHUB_UPLOAD="docker.io/vincinator" ${thisDir}/mk-upload-images.sh  "${GARDENLINUX_BUILD_CRE}" "${VERSION_DATE}" "${VERSION_FULL}" "${TARGET_ARCH}"