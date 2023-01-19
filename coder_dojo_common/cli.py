import json
from datetime import datetime, timedelta
from pprint import pprint
from typing import Dict

import click
import requests

from . import __version__, kenney_assets
from .models import KenneyAssetsModel

from .settings import CoderDojoSettings


@click.group()
@click.version_option(__version__)
def kenney():
    pass


@kenney.command()
def list():
    """
    List kenney assets.

    Displays all assets and their state - whether they have been downloaded and are available.
    """
    coder_dojo_settings = CoderDojoSettings()
    if not coder_dojo_settings.cache_valid:
        coder_dojo_settings.update_cache()

    cached_assets: KenneyAssetsModel = json.load(
        coder_dojo_settings.assets_cache_file.open(encoding="utf-8")
    )




@kenney.command()
def get():
    pass
