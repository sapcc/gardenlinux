#!/usr/bin/env python3

import yaml
import click
import os
import requests
import re
import sys
import glinfo.common as glinfo

def any_match(bykey, byvalue, var):
    if isinstance(var, dict):
        for k,v in var.items():
            if bykey.casefold() in k.casefold() and byvalue.casefold() in v.casefold():
                return True
    return False

@click.command(name="filter")
@click.option("--by", type=(str, str), multiple=True, help='Search package name')
@click.option("--input-yaml", default="packages.yaml", type=click.Path(exists=True), help='Path to packages.yaml generated via fetch command')
def pfilter(by, input_yaml):
    with open(input_yaml, 'r') as file:
        packages_dict = yaml.safe_load(file)

    for fk, fv in by:
        print(f"filtering for {fk}: {fv}")
        for archk in list(packages_dict):
            for pkgk in list(packages_dict[archk]):
                if not glinfo.any_match(fk, fv, packages_dict[archk][pkgk]):
                    del packages_dict[archk][pkgk]

    yaml.dump(packages_dict, sys.stdout)

