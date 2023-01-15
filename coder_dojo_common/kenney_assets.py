from typing import Dict

import bs4.element
from bs4 import BeautifulSoup
from requests import Session


def list_assets(session: Session, base_url: str) -> Dict[str, str]:
    """
    List all assets from the Kenney site.

    :param session: Session to use when making request
    :param base_url: The base assets url for kenney assets
    :return: Dictionary mapping asset to the download url
    """
    page_number = 1
    found_assets = {}
    while True:
        response = session.get(f"{base_url}/page:{page_number}")
        if response.status_code == 404:
            break
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        asset_urls = [
            div.a["href"]
            for div in soup.find_all(id="content")[0].children
            if isinstance(div, bs4.element.Tag)
        ]
        found_assets = {
            **found_assets,
            **{url.split("/")[-1]: url for url in asset_urls},
        }
        page_number += 1
    return found_assets
