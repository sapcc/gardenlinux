# Packagebuild container



## gardenlinux/packagebuild

| Container Tag |  Description  | Dockerfile |
| ------------- |---|---|
| `latest`          | Uses regular debian repos, and `today` of garden linux repo. Used for latest package builds. | [Dockerfile.latest](Dockerfile.latest) | 
| `major.minor`   | Same as latest, but uses snapshot apt repos instead. Used for package builds of previous still supported Garden Linux Versions.  | [Dockerfile.snapshot](Dockerfile.snapshot) | 
| date `YYYYmmdd` | Same as major.minor  | [Dockerfile.snapshot](Dockerfile.snapshot) 


## gardenlinux/packagebuild-lkm

| Container Tag |  Description  | Dockerfile |
| ------------- |---|---|
| `major.minor`     | Based on gardenlinux/packagebuild. Added kernel headers for this Garden Linux version. Used to build loadable kernel modules for Garden Linux. | [Dockerfile.lkm](Dockerfile.lkm) |
| date `YYYYmmdd`   | Same as major.minor | [Dockerfile.lkm](Dockerfile.lkm) |
| `today`           | alias to last `gardenlinux/packagebuild-lkm`. | [Dockerfile.lkm](Dockerfile.lkm) |
