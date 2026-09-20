import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from bs4 import PageElement, Tag, NavigableString
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

PLAYWRIGHT_TIMEOUT = 45_000
PLAYWRIGHT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

MAX_ATTEMPTS = 3


def _get_page(url: str) -> str:
    """Fetch a Newegg page with Chromium."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        raise RuntimeError(
            "Playwright is required for the Newegg scraper."
        ) from error

    last_error = None

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=PLAYWRIGHT_USER_AGENT,
            locale="en-CA",
            viewport={"width": 1366, "height": 900},
        )
        page = context.new_page()

        try:
            for attempt in range(1, MAX_ATTEMPTS + 1):
                try:
                    response = page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=PLAYWRIGHT_TIMEOUT,
                    )

                    if response and response.status >= 400:
                        raise RuntimeError(
                            f"Newegg returned HTTP {response.status}"
                        )

                    page.wait_for_load_state(
                        "networkidle",
                        timeout=15_000,
                    )

                    page.wait_for_selector(
                        ".item-cell, .item-container",
                        timeout=PLAYWRIGHT_TIMEOUT,
                    )

                    return page.content()

                except (PlaywrightTimeoutError, RuntimeError) as error:
                            last_error = error

                            # Preserve evidence of bot pages or markup changes.
                            page.screenshot(
                                path=f"/tmp/newegg-{attempt}.png",
                                full_page=True,
                            )

                            if attempt < MAX_ATTEMPTS:
                                time.sleep(2 ** attempt)

            raise RuntimeError(
                f"Unable to load Newegg page after {MAX_ATTEMPTS} attempts: {url}"
            ) from last_error
        finally:
            browser.close()


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
