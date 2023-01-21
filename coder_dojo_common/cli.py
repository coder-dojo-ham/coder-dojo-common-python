import json
import sys
from pathlib import Path

import click
from colorama import Fore, Style

from . import __version__
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

    cached_assets: KenneyAssetsModel = KenneyAssetsModel(
        **json.load(coder_dojo_settings.assets_cache_file.open(encoding="utf-8"))
    )
    num_lines = 10
    for index, asset in enumerate([asset for asset in cached_assets.assets]):
        if index % num_lines == 0 and index:
            answer = input("Hit any key to continue press q to quit: ")
            if answer.lower() == 'q':
                break
        else:
            print(asset.name)


@kenney.command()
@click.argument("ASSET_NAME")
def install(asset_name):
    coder_dojo_settings = CoderDojoSettings()

    cached_assets: KenneyAssetsModel = KenneyAssetsModel(
        **json.load(coder_dojo_settings.assets_cache_file.open(encoding="utf-8"))
    )

    asset = cached_assets.find(asset_name)

    if not asset:
        print(Fore.RED + f"Unable to find '{asset_name}', please check the spelling" + Style.RESET_ALL)
        print(f"You can run '{Path(sys.argv[0]).name} list' to see all assets")
        sys.exit(1)

    if not asset.archive:
        print(asset)
        # Archive doesn't exist, download
        pass

    asset_path = Path(__file__).parent / f"assets/{asset_name}"
    if not asset_path.exists():
        # Asset not installed, extract and install
        pass
