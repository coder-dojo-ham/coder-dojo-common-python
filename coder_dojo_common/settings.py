from pathlib import Path

from pydantic import BaseSettings


class CoderDojoSettings(BaseSettings):
    root_dir: Path = Path.home() / ".coder_dojo"
    kenney_assets_url: str = "https://kenney.nl/assets"

    class Config:
        env_prefix = "CODER_DOJO_"

    @property
    def downloads(self) -> Path:
        return self.root_dir / "downloads"

    @property
    def kenney_assets(self) -> Path:
        return self.root_dir / "kenney_assets"

    @property
    def assets_cache_file(self) -> Path:
        return self.root_dir / "assets_cache.json"
