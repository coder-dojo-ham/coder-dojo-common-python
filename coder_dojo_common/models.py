from pathlib import Path
from typing import Optional, List, Any, Dict, Union

from pydantic import BaseModel, validator, root_validator


class AssetModel(BaseModel):
    archive: Optional[Path] = None
    local: Optional[Path] = None
    name: str
    url: str

    @root_validator
    @classmethod
    def check_local_install(cls, values) -> Dict[str, Any]:
        asset_path = Path(__file__).parent / f"assets/{values['name']}"
        if asset_path.exists():
            values['local'] = asset_path
        return values


class KenneyAssetsModel(BaseModel):
    assets: List[AssetModel]

    def find(self, asset_name) -> Union[AssetModel,None]:
        found = [asset for asset in self.assets if asset.name == asset_name]
        return found[0] if found else None