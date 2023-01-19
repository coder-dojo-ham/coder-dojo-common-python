from pydantic import BaseSettings


class CoderDojoSettings(BaseSettings):
    kenney_assets_url = "https://kenney.nl/assets"
    class Config:
        env_prefix = "CODER_DOJO_"
