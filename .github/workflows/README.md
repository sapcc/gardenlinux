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

## Package Build Container - gardenlinux/packagebuild
Based on debian slim container image. Additonally provides dependencies for packages builds.
The snapshot version is used, to make the build of previous versions reproducible.

See [../../container/packagebuild/Dockerfile.cross](../../container/packagebuild/Dockerfile.cross)

## Package Build Container with Go - gardenlinux/packagebuild-go
Based on `gardenlinux/packagebuild` with added go runtime.

See [../../container/packagebuild/Dockerfile.go.cross](../../container/packagebuild/Dockerfile.go.cross)

## Package Build Container LKM - gardenlinux/packagebuild-lkm
Based on `gardenlinux/packagebuild` with added tools to retreive the respective kernel version of the given Garden Linux Version.

Garden Linux apt key is trusted, and repo.gardenlinux.io is added to the apt sources. This is required to install the kernel headers.

This wrapper outputs the latest installed kernel header in that container.
Original uname is moved to /bin/uname-orig, and `bin/uname` is a wrapper that outputs the correct header version installed when using `uname -r`. 
This allows to build kernel modules in a container, where the host is not a Garden Linux.

See [../../container/packagebuild/Dockerfile.go.cross](../../container/packagebuild/Dockerfile.go.cross)
