#!/usr/bin/env python3
import click


from glinfo.fetch import fetch
from glinfo.search import search

@click.group()
def entry_point():
    pass

entry_point.add_command(fetch)
entry_point.add_command(search)


if __name__ == '__main__':
    entry_point()
