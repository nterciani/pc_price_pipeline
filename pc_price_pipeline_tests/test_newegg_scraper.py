from pc_price_pipeline.scrapers.newegg import *
from pathlib import Path
from unittest.mock import patch
import pytest

newegg_amd_mobo_path = "test_assets/newegg_amd_motherboards.html"

@patch('pc_price_pipeline.scrapers.newegg._get_page')
def test_get_pages(mock_get_page):
    html_path = Path(__file__).parent / "test_assets" / "newegg_amd_motherboards.html"
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    mock_get_page.return_value = html
    
    result = get_newegg_pages("https://example.com/mobos")
    
    assert result == 5


@patch('pc_price_pipeline.scrapers.newegg._get_page')
def test_get_pages_no_pagination(mock_get_page):
    html = "<html><body>No pagination here</body></html>"

    mock_get_page.return_value = html

    with pytest.raises(ValueError):
        get_newegg_pages("https://example.com/mobos")

    
@patch('pc_price_pipeline.scrapers.newegg._get_page')
def test_get_pages_no_pagination_with_item(mock_get_page):
    html = """<html><body><div class="item-cell" id="item_cell_13-119-709_2_0"></body></html>"""

    mock_get_page.return_value = html

    result = get_newegg_pages("https://example.com/mobos")

    assert result == 1


