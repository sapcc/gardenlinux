#!/usr/bin/env python3

import yaml
import click
import os
import requests
import re

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



def any_match(bykey, byvalue, var):
    if isinstance(var, dict):
        for k,v in var.items():
            if bykey.casefold() in k.casefold() and byvalue.casefold() in v.casefold():
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

