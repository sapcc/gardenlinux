


# Initialize env for development

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

# Commands


## Fetch
Downloads package info from repo.gardenlinux.io, fetches packages included by features
and combines this information in a `packages.yaml` file.

This file is required for the other commands of garden-package-info.
TODO: automatically run fetch for other commands if packages.yaml is not available.


## filter
Outputs a list of packages filtered by (multiple) attributes. The output contains not only 
the names, but also for each packet available attributes. Available attributes can be 
configured in the glinfo/fetch.py.


```
# General:
./garden-package-info filter --by attributekey value
# Example:
./garden-package-info filter --by Architecture amd64
```


## cve

work in progress, currently not working

## search

work in progress, currently not working
