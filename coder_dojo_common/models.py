from pathlib import Path
from typing import Optional, List

from pydantic import BaseModel


class AssetModel(BaseModel):
    archive: Optional[Path] = None
    local: Optional[Path] = None
    name: str
    url: str


class KenneyAssetsModel(BaseModel):
    assets: List[AssetModel]


