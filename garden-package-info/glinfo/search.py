#!/usr/bin/env python3

import yaml
import click
import os
import requests
import re
import glinfo.common as gli



@click.command()
@click.option("--package", required=True, help='Search package name')
@click.option("--input-yaml", default="packages.yaml", type=click.Path(exists=True), help='Path to packages.yaml generated via fetch command')
def search(package, input_yaml):

    with open(input_yaml, 'r') as file:
        packages_dict = yaml.safe_load(file)

    for result in glinfo.gen_dict_extract(package, packages_dict):
        print(f"Package: {package}")
        print(yaml.dump(result))

