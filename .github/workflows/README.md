# Workflows

## Dev
Runs on `push` and `pull_request` (enabled for branches created by Garden Linux Developer)
1. Build Garden Linux Images

See [dev.yml](dev.yml) for implementation details.

## Nightly
Runs every day (enabled only for main branch):

1. Build packagebuild container
1. Builds Garden Linux images
1. On successful build, images are uploaded to S3

See [nightly.yml](nightly.yml) for implementation details. 

## Beta Release
Runs weekly on main branch
1. Builds Garden Linux images
1. Build integration test container
1. Runs platform tests for each supported platform 
<!-- 1. On successful tests, images are handed over to Tekton Pipeline for publishing -->
1. Creates git tag `beta-<Major>.<Minor>` (for tested HEAD of main)

See [beta.yml](beta.yml) for implementation details. 

## Stable Release
Runs on push to a release branch (enabled for `stable-**` branches)

Stable branches must be manually created.

1. Builds Garden Linux images
1. Build integration test container
1. Runs platform tests for each supported platform 
1. On successful tests, images are handed over to Tekton Pipeline for publishing

See [stable.yml](stable.yml) for implementation details. 


# Container

## Integration test Container - gardenlinux/integration-test
Provides dependencies for running tests on the cloud platforms.

See [container-integrationtest.yml](container-integrationtest.yml)

## Package Build Container - gardenlinux/packagebuild-<arm64/amd64>
Based on debian slim container image. Additonally provides dependencies for packages builds.
The snapshot version is used, to make the build of previous versions reproducible.

First, a packagebuild container will be built normally with the default debian repositories. 
In a second step, this container will be the base for a snapshot version of packagebuild.

The snapshot version has fixed snapshot repos configured in `/etc/apt/sources.list`,
while the `latest` version of `gardenlinux/packagebuild` uses the default debian repos and the today suite of Garden Linux repo.

See [../../container/packagebuild/Dockerfile.latest](../../container/packagebuild/Dockerfile.latest) and [../../container/packagebuild/Dockerfile.snapshot](../../container/packagebuild/Dockerfile.snapshot).

Snapshot versions are tagged with the major.minor version of Garden Linux and additionally with the date in the format `YYYYmmdd`.
Latest version should be used by default by the package build pipelines. For legacy builds, the snapshot version of the container is used.
Please note that the debian snapshot repos have a rate limit.

## Package Build Container LKM - gardenlinux/packagebuild-lkm
Based on `gardenlinux/packagebuild` with added tools to retreive the respective kernel version of the given Garden Linux Version.

Original uname is moved to /bin/uname-orig, and `bin/uname` is a wrapper that outputs the correct header version installed when using `uname -r`. 
This allows to build kernel modules in a container, where the host is not a Garden Linux.

See [../../container/packagebuild/Dockerfile.lkm](../../container/packagebuild/Dockerfile.lkm)
