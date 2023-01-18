import json
from datetime import datetime, timedelta
from pathlib import Path

import requests
from pydantic import BaseSettings, validator

from coder_dojo_common import kenney_assets


class CoderDojoSettings(BaseSettings):
    cache_expiry_days: int = 14
    root_dir: Path = Path.home() / ".coder_dojo"
    kenney_assets_url: str = "https://kenney.nl/assets"

    # Configuration
    class Config:
        """
        Set env prefix, root values cane be overriden from environment variables prefixed with CODER_DOJO_

        e.g.
            CODER_DOJO_ROOT_DIR=/tmp
        """

        env_prefix = "CODER_DOJO_"

    # Class methods
    @validator("root_dir")
    @classmethod
    def create_dir(cls, value: Path):
        """Triggers after root_dir is cast to Path -> creates directory"""
        value.mkdir(exist_ok=True, parents=True)
        return value

    # Properties
    @property
    def assets_cache_file(self) -> Path:
        """File to cache asset information"""
        return self.root_dir / "assets_cache.json"

    @property
    def cache_valid(self) -> bool:
        """Returns true if cache is valid (it exists and is recent), false if not"""
        return self.assets_cache_file.exists() and datetime.fromtimestamp(
            self.assets_cache_file.stat().st_mtime
        ) > datetime.now() - timedelta(days=self.cache_expiry_days)

    @property
    def downloads_path(self) -> Path:
        """The path to use for downloads"""
        return self.root_dir / "downloads"

    @property
    def kenney_assets_path(self) -> Path:
        """Folder containing extracted assets"""
        return self.root_dir / "kenney_assets"

    # Methods
    def update_cache(self) -> None:
        """
        One shot call to update the cache
        :return: None
        """

        session = requests.Session()
        assets = kenney_assets.get_assets(
            session=session, base_url=self.kenney_assets_url
        )
        self.assets_cache_file.write_text(
            json.dumps(assets.dict(), indent=4, sort_keys=True)
        )
