import requests
from bs4 import BeautifulSoup
from bs4 import PageElement, Tag, NavigableString
import pandas as pd
import time
import random

def get_newegg_pages(url: str) -> int:
    """Returns the number of pages for a Newegg Pc part."""
    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    pagination_span = soup.find(name="span", class_="list-tool-pagination-text")

    if not pagination_span:
        items = soup.select(".item-cell")
        if items:
            return 1 # single page of results
        else:
            # no items and no pagination
            raise ValueError(
                f"No pagination or items found at {url}. "
                "Possible causes: bot detection, invalid URL, or site structure changed."
            )

    pages_tag = pagination_span.find(name="strong")
    if not pages_tag:
        raise ValueError(f"Pagination element found but missing page count at {url}")
    
    last_page_number = int(pages_tag.text.split('/')[-1])
    return last_page_number

def parse_price(element: PageElement | Tag | NavigableString) -> str:
    try:  # make sure price exists
        price_dollars = element.find(name="li", class_="price-current").find(name="strong").text.replace(",", "")
        price_cents = element.find(name="li", class_="price-current").find(name="sup").text
        price = price_dollars + price_cents  # current price with discounts
    except:
        price = "0"

    return price

def scrape_newegg_category(category: str, url: str) -> list[dict]:
    """
    Scrapes raw pricing data from Newegg given a category.
    This data is unvalidated and may contain errors.
    """
    rows = []
    pages = get_newegg_pages(url)

    for page in range(1, pages + 1):
        response = requests.get(f"{url}&page={page}")
        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.select(".item-cell")
        if not items:
            break # no more pages

        for item in items:
            rows.append({
                "raw_name": item.select_one(".item-title").text.strip(),
                "raw_price": float(parse_price(item)),
                "store": "Newegg",
                "category": category,
                "scraped_at": pd.Timestamp.utcnow(),
                "source_url": item.select_one(".item-title").get(key="href"),
            })

        page += 1
        time.sleep(random.uniform(1.5, 3.0))  # limit scraping rate

    return rows
