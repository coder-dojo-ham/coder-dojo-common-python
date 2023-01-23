from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel
from requests import Session

from coder_dojo_common import kenney_assets


class Asset(BaseModel):
    archive: Optional[Path] = None
    local: Optional[Path] = None
    url: str

    # @root_validator
    # @classmethod
    # def check_local_install(cls, values) -> Dict[str, Any]:
    #     asset_path = Path(__file__).parent / f"assets/{values['name']}"
    #     if asset_path.exists():
    #         values['local'] = asset_path
    #     return values


class KenneyAssets():

    def __init__(self, root_dir: Path):
        self._assets = {}
        self._root_dir = root_dir
        self._session = Session()
        self.kenney_assets_url = "https://kenney.nl/assets"

        self.cache_file = self._root_dir / "assets_cache.json"

        if not self.cache_valid:
            self.update_cache()

        self._update_asset_model()

    def __iter__(self) -> list[str]:
        return iter(k for k in self._assets)

    def __getitem__(self, item) -> Union[Asset, None]:
        if asset := self._assets.get(item):
            return Asset(**asset)

        return None

    def download(self, asset_name: str):
        asset: Asset = self[asset_name]
        asset_download_link = kenney_assets.get_download_link(self._session, asset.url)
        zip_response = self._session.get(asset_download_link, stream=True)
        asset.archive = Path(self._root_dir / f"downloads/{asset_name}.zip")
        asset.archive.write_bytes(zip_response.content)
        self._assets[asset_name] = json.loads(asset.json())
        self.save_asset_cache()

    @property
    def cache_valid(self) -> bool:
        return self.cache_file.exists() and datetime.fromtimestamp(
            self.cache_file.stat().st_mtime) > datetime.now() - timedelta(days=14)

    def _update_asset_model(self):
        self._assets = json.load(self.cache_file.open())

    def update_cache(self):
        print("Updating cache...")
        assets = kenney_assets.get_assets(
            session=self._session, base_url=self.kenney_assets_url
        )
        self.cache_file.write_text(
            json.dumps(assets, indent=4, sort_keys=True)
        )

    def save_asset_cache(self):
        self.cache_file.write_text(
            json.dumps(self._assets, indent=4, sort_keys=True)
        )
