# PC Market Viewer

An educational data engineering project that collects PC component prices,
normalizes product metadata, matches products over time, and stores the results
in BigQuery for historical analysis.

The pipeline currently runs daily through Dagster and GitHub Actions. Its main
source is Newegg Canada.

## Current Architecture

```text
Newegg Canada
      |
      v
Playwright scraper
      |
      v
Dagster assets
      |
      +--> raw prices
      +--> cleaned prices
      +--> category-specific product attributes
      +--> product embeddings and vector matching
      |
      v
BigQuery star schema
```

## Implemented Features

### Extraction

- Scrapes CPUs, GPUs, motherboards, memory, PSUs, and storage.
- Uses Chromium through Playwright because Newegg challenges plain HTTP clients.
- Uses a fresh headless Chromium browser for each fetched page.
- Records product name, price, retailer, category, timestamp, and source URL.

### Transformation

- Cleans prices, names, timestamps, URLs, and duplicate observations.
- Extracts category-specific attributes from product titles.
- Supports CPU, GPU, memory, motherboard, PSU, and storage schemas.
- Generates stable product keys from normalized product attributes.
- Flags records that need review when metadata extraction is incomplete.

### Warehouse Model

The pipeline uses a shared star-schema model:

- `dim_products`: product name, brand, category, and embedding.
- `dim_*_specs`: category-specific product attributes.
- `dim_retailers`: retailer name, domain, country.
- `fact_prices`: historical price observations by product and retailer.
- `fact_vector_search`: product matching confidence, method, and approval state.

The project also retains raw and intermediate data during the asset pipeline for
debugging and transformation boundaries.

### Product Matching

- Loads the embedding model once per Python process with `lru_cache`.
- Generates normalized product embeddings.
- Uses BigQuery vector search to match incoming products to existing products.
- Preserves match confidence and approval metadata for review.

### Orchestration and Automation

- Dagster assets are grouped by component category.
- `daily_etl_job` selects all assets.
- GitHub Actions runs the ingest job daily at 06:07 UTC and supports manual runs.
- CI installs both the Playwright Python package and the Chromium runtime.

## Data Flow

1. Scrape raw Newegg listings.
2. Clean and validate common price fields.
3. Extract product names and category specifications.
4. Generate stable product keys and embeddings.
5. Match products against existing BigQuery products.
6. Split records into product, specification, price, and matching tables.
7. Append the current price snapshot to BigQuery.

## Setup

Requirements: Python 3.10-3.14, Google Cloud credentials with BigQuery access,
and a Playwright-compatible Chromium installation.

```bash
pip install -e .
python -m playwright install chromium
```

On Ubuntu or GitHub Actions, install Chromium's system dependencies too:

```bash
python -m playwright install --with-deps chromium
```

Set `GOOGLE_APPLICATION_CREDENTIALS` to the service-account JSON file before
running the pipeline.
