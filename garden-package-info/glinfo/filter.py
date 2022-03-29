#!/usr/bin/env python3

import yaml
import click
import os
import requests
import re
import sys
import glinfo.common as glinfo


@click.command(name="filter")
@click.option("--by", type=(str, str), multiple=True, help='Search package name')
@click.option("--select", type=str, multiple=True, help='Only include given attributes in output')
@click.option("--only-names", is_flag=True, default=False, help='Only include names in output, no attributes')
@click.option("--input-yaml", default="packages.yaml", type=click.Path(exists=True), help='Path to packages.yaml generated via fetch command')
def pfilter(by, select, only_names, input_yaml):
    with open(input_yaml, 'r') as file:
        packages_dict = yaml.safe_load(file)

    for fk, fv in by:
        print(f"filtering for {fk}: {fv}")
        for archk in list(packages_dict):
            for pkgk in list(packages_dict[archk]):
                if not glinfo.any_match(fk, fv, packages_dict[archk][pkgk]):
                    del packages_dict[archk][pkgk]

    if select:
        for archk in list(packages_dict):
            for pkgk in list(packages_dict[archk]):
                for attribute in list(packages_dict[archk][pkgk]):
                    if only_names:
                        del packages_dict[archk][pkgk][attribute]
                        continue
                    if not attribute in select:
                        del packages_dict[archk][pkgk][attribute]


    yaml.dump(packages_dict, sys.stdout)

