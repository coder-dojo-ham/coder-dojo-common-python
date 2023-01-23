from pprint import pprint
from typing import Dict

import bs4.element
from bs4 import BeautifulSoup
from requests import Session


def get_assets(session: Session, base_url: str) -> Dict[str, str]:
    """
    Get all assets from the Kenney site.
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
        found_assets = {**found_assets, **{url.split("/")[-1]: {"url": url} for url in asset_urls}}
        page_number += 1
    return found_assets


def get_download_link(session: Session, asset_url: str) -> str:
    response = session.get(asset_url)
    soup = BeautifulSoup(response.text, "html.parser")
    anchors = soup.find_all("a")
    for anchor in anchors:
        if ".zip" in anchor["href"]:
            return anchor["href"]
