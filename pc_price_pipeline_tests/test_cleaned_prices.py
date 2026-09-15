import pandas as pd

from pc_price_pipeline.assets.common.cleaned_prices import cleaned_prices_df


def test_cleaned_prices_filters_invalid_and_combo_rows():
    raw = pd.DataFrame(
        {
            "raw_name": ["  Product   A  ", "Product B", "Product C"],
            "raw_price": [10.0, 0.0, None],
            "store": ["Newegg", "Newegg", "Newegg"],
            "category": ["CPU", "CPU", "CPU"],
            "scraped_at": pd.to_datetime(["2026-01-25 10:00", "2026-01-25 10:05", "2026-01-25 10:10"], utc=True),
            "source_url": ["https://example/a", "https://example/b", "https://example/ComboDeal/c"],
        }
    )

    result = cleaned_prices_df(raw)

    assert result["raw_name"].tolist() == ["Product A"]
    assert result["price"].tolist() == [10.0]
    assert "scrape_window" not in result.columns


def test_cleaned_prices_deduplicates_within_hour_but_keeps_later_observation():
    raw = pd.DataFrame(
        {
            "raw_name": ["Product A", "Product A", "Product A"],
            "raw_price": [10.0, 11.0, 12.0],
            "store": ["Newegg"] * 3,
            "category": ["CPU"] * 3,
            "scraped_at": pd.to_datetime(
                ["2026-01-25 10:00", "2026-01-25 10:45", "2026-01-25 11:00"], utc=True
            ),
            "source_url": ["https://example/a"] * 3,
        }
    )

    result = cleaned_prices_df(raw)

    assert len(result) == 2
    assert result["price"].tolist() == [10.0, 12.0]
