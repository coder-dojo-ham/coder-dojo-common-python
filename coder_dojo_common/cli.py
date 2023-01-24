"""Basic CLI for managing Kenney assets"""

import sys
import zipfile
from pathlib import Path

import click
from colorama import Fore, Style

from . import __version__
from .models import KenneyAssets
from .settings import CoderDojoSettings


@click.group()
@click.version_option(__version__)
def kenney():
    """Basic CLI to help use kenney.nl assets."""


@kenney.command()
def query():
    """
    List kenney.nl assets.

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
    """
    Download and install kenney.nl asset.

    Will install either the cached archive or latest version from kenney.nl into the 'assets'
    folder in the current directory.
    """
    coder_dojo_settings = CoderDojoSettings()
    asset_path = Path(f"assets/{asset_name}")

    if asset_path.exists():
        print(
            Fore.RED
            + f"'{asset_name}' already installed in '{asset_path.absolute()}'."
            + Style.RESET_ALL
        )

    assets = KenneyAssets(root_dir=coder_dojo_settings.root_dir)

    asset = assets[asset_name]

    if not asset:
        print(
            Fore.RED
            + f"Unable to find '{asset_name}', please check the spelling."
            + Style.RESET_ALL
        )
        print(f"You can run '{Path(sys.argv[0]).name} query' to see all assets")
        sys.exit(1)

    if not asset.archive:
        print(
            Fore.YELLOW + f"Downloading '{asset_name}', please wait" + Style.RESET_ALL
        )
        assets.download(asset_name)

    asset = assets[asset_name]
    print(
        Fore.GREEN
        + f"Installing '{asset_name}' into {asset_path.absolute()}"
        + Style.RESET_ALL
    )
    asset_path.mkdir(parents=True)
    with zipfile.ZipFile(asset.archive, "r") as zip_file:
        zip_file.extractall(asset_path.absolute())
