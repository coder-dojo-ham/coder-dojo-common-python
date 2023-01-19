from pprint import pprint

import click
import requests

from . import __version__


@click.group()
@click.version_option(__version__)
def kenney():
    pass


@kenney.command()
def list():
    response = requests.get("https://kenney.nl/assets")

    pprint(response.text)
    pass


@kenney.command()
def get():
    pass


