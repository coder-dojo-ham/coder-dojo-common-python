from pathlib import Path

from pydantic import BaseSettings, validator


class CoderDojoSettings(BaseSettings):
    root_dir: Path = Path.home() / ".coder_dojo"

    # Configuration
    class Config:
        """
        Set env prefix, root values can be overridden from environment variables prefixed with CODER_DOJO_

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
        (value / "downloads").mkdir(exist_ok=True, parents=True)
        return value
