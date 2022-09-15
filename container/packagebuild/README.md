# Packagebuild container



## gardenlinux/packagebuild

| Container Tag |  Description  | 
| ------------- |---|
| `latest`          | Uses regular debian repos, and `today` of garden linux repo. Used for latest package builds. | 
| `major.minor`   | Same as latest, but uses snapshot apt repos instead. Used for package builds of previous still supported Garden Linux Versions.  | 
| date `YYYYmmdd` | Same as major.minor  | 


## gardenlinux/packagebuild-lkm

| Container Tag |  Description  | 
| ------------- |---|
| `major.minor`     | Based on gardenlinux/packagebuild. Added kernel headers for this Garden Linux version. Used to build loadable kernel modules for Garden Linux. | 
| date `YYYYmmdd`   | Same as major.minor | 
| `today`           | alias to last `gardenlinux/packagebuild-lkm`. | 
