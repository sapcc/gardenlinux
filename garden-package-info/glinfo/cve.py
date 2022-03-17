#!/usr/bin/env python3

import yaml
import click
import os
import requests
import re
import glinfo.common as glinfo
import json


def cve_jfilter_status_open(dist, json):
    for pkg_key, pkg_dict in json.items():
        for cve_key, cve_dict in pkg_dict.items():
            if cve_dict["releases"][dist]["status"] == "open":
                yield { cve_key: cve_dict }

def fetch_debian_cve_json():
    url = "https://security-tracker.debian.org/tracker/data/json"
    return json.loads(glinfo.download_file(url))


@click.command()
@click.option("--package", help='Search package name')
@click.option("--dist", default="bookworm", help='Debian Distribution')
@click.option("--input-yaml", default="packages.yaml", type=click.Path(exists=True), help='Path to packages.yaml generated via fetch command')
def cve(package, dist, input_yaml):

    with open(input_yaml, 'r') as file:
        packages_dict = yaml.safe_load(file)

    if package:
        if not glinfo.has_package(package, packages_dict):
            print("Package does not exist in gardenlinux")
            return

    json = fetch_debian_cve_json()
    if package:
        json = { package: json[package] }

    for pkg in cve_jfilter_status_open(dist, json):
        print(pkg)


