#!/bin/bash

set -Eeuo pipefail
thisDir="$(dirname "$(readlink -f "$BASH_SOURCE")")"

GARDENLINUX_BUILD_CRE=${1}
VERSION_DATE=${2}
VERSION_FULL=${3}
TARGET_ARCH=${4}


USAGE="Usage: $0 <gardenlinux-build-cre> <version-date> <major.minor> <target arch>"

[ -z "$GARDENLINUX_BUILD_CRE" ] && echo "$USAGE" && exit 1
[ -z "$VERSION_DATE" ] && echo "$USAGE" && exit 1
[ -z "$VERSION_FULL" ] && echo "$USAGE" && exit 1
[ -z "$TARGET_ARCH" ] && echo "$USAGE" && exit 1


if [ -v DOCKERHUB_UPLOAD ];then

    ${GARDENLINUX_BUILD_CRE} tag "gardenlinux/packagebuild-${TARGET_ARCH}:latest" "${DOCKERHUB_UPLOAD}/packagebuild-${TARGET_ARCH}:latest"
    ${GARDENLINUX_BUILD_CRE} push "${DOCKERHUB_UPLOAD}/packagebuild-${TARGET_ARCH}:latest"

    ${GARDENLINUX_BUILD_CRE} tag "gardenlinux/packagebuild-${TARGET_ARCH}:${VERSION_FULL}" "${DOCKERHUB_UPLOAD}/packagebuild-${TARGET_ARCH}:${VERSION_FULL}"
    ${GARDENLINUX_BUILD_CRE} tag "gardenlinux/packagebuild-${TARGET_ARCH}:${VERSION_DATE}" "${DOCKERHUB_UPLOAD}/packagebuild-${TARGET_ARCH}:${VERSION_DATE}"
    ${GARDENLINUX_BUILD_CRE} push "${DOCKERHUB_UPLOAD}/packagebuild-${TARGET_ARCH}:${VERSION_FULL}"
    ${GARDENLINUX_BUILD_CRE} push "${DOCKERHUB_UPLOAD}/packagebuild-${TARGET_ARCH}:${VERSION_DATE}"

    ${GARDENLINUX_BUILD_CRE} tag "gardenlinux/packagebuild-lkm-${TARGET_ARCH}:${VERSION_FULL}" "${DOCKERHUB_UPLOAD}/packagebuild-lkm-${TARGET_ARCH}:${VERSION_FULL}"
    ${GARDENLINUX_BUILD_CRE} tag "gardenlinux/packagebuild-lkm-${TARGET_ARCH}:${VERSION_DATE}" "${DOCKERHUB_UPLOAD}/packagebuild-lkm-${TARGET_ARCH}:${VERSION_DATE}"
    ${GARDENLINUX_BUILD_CRE} push "${DOCKERHUB_UPLOAD}/packagebuild-lkm-${TARGET_ARCH}:${VERSION_FULL}"
    ${GARDENLINUX_BUILD_CRE} push "${DOCKERHUB_UPLOAD}/packagebuild-lkm-${TARGET_ARCH}:${VERSION_DATE}"

fi


# Uploading the images in this script (instead of github actions) allows to easily upload them also manually if required. 
# Requirements: GHCR_UPLOAD variable is set, and user is logged in to ghcr
if [ -v GHCR_UPLOAD ];then
    # push the latest version
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild-${TARGET_ARCH}:latest"
    
    # push the snapshot version (two aliases)
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild-${TARGET_ARCH}:${VERSION_FULL}"
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild-${TARGET_ARCH}:${VERSION_DATE}"

    # push the lkm version (three aliases)
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild-lkm-${TARGET_ARCH}:${VERSION_FULL}"
    ${GARDENLINUX_BUILD_CRE} push "ghcr.io/gardenlinux/gardenlinux/packagebuild-lkm-${TARGET_ARCH}:${VERSION_DATE}"
fi