#!/usr/bin/env python3

import yaml
import click
import os
import requests
import gzip
import re

# Some consts
GLINFO_ARCHICTECTURES = ["all", "amd64", "arm64"]

def has_package(name, var):
    for arch in var:
        if name in var[arch]:
            return True
    return False

def download_file(url):
    resp = requests.get(url)
    content = resp.content.decode("utf-8")
    for line in content.splitlines():
            if re.search("<Error><Code>NoSuchKey</Code>",line):
                raise Exception('Repo not found')
    return content

def download_archive_file(url):
    resp = requests.get(url)

    if resp.status_code == 404:
        raise Exception('Repo not found')

    try:
        content = gzip.decompress(resp.content).decode("utf-8")
    except:
        print("Error")
    return content

def any_match(key, value, var):
    """
    Check if var (dict) contains the given
    key value pair.
    """
    if not isinstance(var, dict):
        return False

    # Get value from var
    var_value = None
    for k,v in var.items():
        if k.casefold() == key.casefold():
            var_value = v

    # If var does not contain our
    # value, we can stop it here
    if not var_value:
        return False

    # If value is set to any,
    # there is always a match
    if value.casefold() == "any":
        return True

    # If var value (string) equals the passed value,
    # there is a match.
    if not isinstance(var_value, list) and value.casefold() == var_value.casefold():
        return True

    # If var value (list) contains the passed value,
    # there is a match, too.
    if isinstance(var_value, list) and value.casefold() in var_value:
        return True

    return False

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

