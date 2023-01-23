import sys
from pathlib import Path

import click
from colorama import Fore, Style

from . import __version__
from .models import KenneyAssets
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
    assets = KenneyAssets(root_dir=coder_dojo_settings.root_dir)
    if not assets.cache_valid:
        assets.update_cache()

    for asset in assets:
        print(asset)


@kenney.command()
@click.argument("ASSET_NAME")
def install(asset_name):
    coder_dojo_settings = CoderDojoSettings()
    assets = KenneyAssets(root_dir=coder_dojo_settings.root_dir)

    asset = assets[asset_name]

    if not asset:
        print(Fore.RED + f"Unable to find '{asset_name}', please check the spelling" + Style.RESET_ALL)
        print(f"You can run '{Path(sys.argv[0]).name} list' to see all assets")
        sys.exit(1)

    if not asset.archive:
        assets.download(asset_name)

    asset_path = Path(__file__).parent / f"assets/{asset_name}"
    if not asset_path.exists():
        # Asset not installed, extract and install
        pass
