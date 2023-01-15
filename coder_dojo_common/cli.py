import json
from datetime import datetime, timedelta
from pprint import pprint

import click
import requests

from . import __version__, kenney_assets
from .settings import CoderDojoSettings


@click.group()
@click.version_option(__version__)
def kenney():
    pass


@kenney.command()
def list():
    coder_dojo_settings = CoderDojoSettings()
    coder_dojo_settings.root_dir.mkdir(exist_ok=True, parents=True)
    if not coder_dojo_settings.assets_cache_file.exists() or datetime.fromtimestamp(
        coder_dojo_settings.assets_cache_file.stat().st_mtime
    ) < datetime.now() - timedelta(days=14):
        session = requests.Session()
        assets = kenney_assets.list_assets(
            session=session, base_url=coder_dojo_settings.kenney_assets_url
        )
        coder_dojo_settings.assets_cache_file.write_text(
            json.dumps(assets, indent=4, sort_keys=True)
        )
    cached_assets = json.load(
        coder_dojo_settings.assets_cache_file.open(encoding="utf-8")
    )

    pprint(cached_assets)


@kenney.command()
def get():
    pass
