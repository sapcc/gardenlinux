#!/usr/bin/env python3
import click


from glinfo.fetch import fetch
from glinfo.search import search
from glinfo.filter import pfilter
from glinfo.cve import cve

@click.group()
def entry_point():
    pass

entry_point.add_command(fetch)
entry_point.add_command(search)
entry_point.add_command(pfilter)
entry_point.add_command(cve)


if __name__ == '__main__':
    entry_point()
