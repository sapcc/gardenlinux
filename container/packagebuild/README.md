# Packagebuild container

The package build container has the goal to assure reproducability of old Garden Linux versions, 
by providing build container images with locked build dependencies.

While allmost all build dependencies can be retrieved via Debian Snapshot repositories,
or snapshot versions of debian images on dockerhub, 
this packagebuild container assures independency to deliver the promise of repeatable and auditable builds.


## gardenlinux/packagebuild

This container image comes in two variants. The difference between those variants is only the `/etc/apt/sources.list`. 
The debian snapshot repositories have a rate limit, so the default of building nightly is to use build container with 
regular debian repos that do not have the rate limit.

| Container Tag |  Description  | Dockerfile |
| ------------- |---|---|
| `latest`          | Uses regular debian repos, and `today` of garden linux repo. Used for nightly package builds. | [Dockerfile.latest](Dockerfile.latest) | 
| `major.minor`   | Same as latest, but uses snapshot apt repos instead. Used for package builds of previous still supported Garden Linux Versions.  | [Dockerfile.snapshot](Dockerfile.snapshot) | 
| date `YYYYmmdd` | Same as major.minor  | [Dockerfile.snapshot](Dockerfile.snapshot) 


## gardenlinux/packagebuild-lkm

| Container Tag |  Description  | Dockerfile |
| ------------- |---|---|
| `major.minor`     | Based on gardenlinux/packagebuild. Added kernel headers for this Garden Linux version. Used to build loadable kernel modules for Garden Linux. | [Dockerfile.lkm](Dockerfile.lkm) |
| date `YYYYmmdd`   | Same as major.minor | [Dockerfile.lkm](Dockerfile.lkm) |
| `today`           | alias to last `gardenlinux/packagebuild-lkm`. | [Dockerfile.lkm](Dockerfile.lkm) |
