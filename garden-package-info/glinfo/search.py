#!/usr/bin/env python3

import yaml
import click
import os
import requests
import re



def gen_dict_extract(key, var):
    if isinstance(var, dict):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                yield from gen_dict_extract(key, v)


def load_yaml(fname):
    with open(fname, 'r') as file:
        packages_dict = yaml.safe_load(file)
    return packages_dict

@click.command()
@click.option("--package", help='Search package name')
@click.option("--input-yaml", default="packages.yaml", type=click.Path(exists=True), help='Path to packages.yaml generated via fetch command')
def search(package, input_yaml):
    with open(input_yaml, 'r') as file:
        packages_dict = yaml.safe_load(file)

    for result in gen_dict_extract(package, packages_dict):
        print(f"Package: {package}")
        print(yaml.dump(result))

