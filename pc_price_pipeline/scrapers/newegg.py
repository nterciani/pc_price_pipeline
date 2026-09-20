import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from curl_cffi import requests
from bs4 import PageElement, Tag, NavigableString

HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


def _get_page(url: str) -> str:
    """Fetch a Newegg page with curl."""
    try:
        response = requests.get(
            url, 
            headers=HEADERS, 
            impersonate="chrome124",
            timeout=15
        )

        if response.status_code == 200:
            return response.text
        else:
            raise RuntimeError(f"Failed to fetch page {url}: Status code {response.status_code}")

    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch page {url}: {e}")


def get_newegg_pages(url: str) -> int:
    """Returns the number of pages for a Newegg PC part."""
    soup = BeautifulSoup(_get_page(url), "html.parser")

    pagination_span = soup.find(name="span", class_="list-tool-pagination-text")

    if not pagination_span:
        items = soup.select(".item-cell")
        if items:
            return 1
        raise ValueError(f"No items found at {url}.")

    pages_tag = pagination_span.find(name="strong")
    if not pages_tag:
        raise ValueError(f"Pagination element found but missing page count at {url}")

    return int(pages_tag.text.split("/")[-1])


def parse_price(element: PageElement | Tag | NavigableString) -> str:
    try:
        price = element.find(name="li", class_="price-current")
        dollars = price.find(name="strong").text.replace(",", "")
        cents = price.find(name="sup").text
        return dollars + cents
    except (AttributeError, TypeError):
        return "0"


def scrape_newegg_category(category: str, url: str) -> list[dict]:
    """Scrape raw pricing data from a Newegg category."""
    rows = []
    pages = get_newegg_pages(url)

    for page_number in range(1, pages + 1):
        soup = BeautifulSoup(
            _get_page(f"{url}&page={page_number}"),
            "html.parser",
        )
        items = soup.select(".item-cell, .item-container")
        if not items:
            break

        for item in items:
            rows.append({
                "raw_name": item.select_one(".item-title").text.strip(),
                "raw_price": float(parse_price(item)),
                "store": "Newegg",
                "category": category,
                "scraped_at": pd.Timestamp.utcnow(),
                "source_url": item.select_one(".item-title").get(key="href"),
            })

        time.sleep(random.uniform(1.5, 3.0))

    return rows
