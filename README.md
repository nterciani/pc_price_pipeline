# PC Component Price Data Pipeline

Educational project that implements an ETL data pipeline, orchestrated with Dagster and stored in Google BigQuery. 

The pipeline scrapes PC component data & pricing from online retailers, cleans and enriches
product metadata, and stores historical price snapshots in Google BigQuery for long-term price
analysis. 

The pipeline is orchestrated with Dagster, implemented in Python, and designed to support multiple 
retailers, component categories, and daily price tracking.

## Features
- Scrapes PC component listings (CPUs, GPUs, motherboards, memory, storage, PSUs)
- Cleans and normalizes raw listing data using Pandas
- Enriches products by extracting structured specifications from listing titles
- Assigns stable `product_id`s to enable price tracking over time
- Stores historical price snapshots in Google BigQuery
- Modular asset-based design using Dagster
- Unit-tested transformation logic with pytest

## Pipeline Overview
1. **Extract**
   * Scrape raw product listings and prices from retailer category pages.
2. **Clean**
   * Normalize fields (price, store, category, timestamps) and remove invalid records.
3. **Enrich**
   * Parse structured attributes (e.g. brand, socket, chipset, memory type) from raw product names and generate stable product identifiers.
4. **Load**
   * Write enriched price snapshots to BigQuery tables partitioned by component category.

## Data Model
Each record in BigQuery represents a price snapshot of a specific product at a specific point in time.
- `product_id` is derived from a normalized product family and remains stable across scrapes
- Multiple records per product are intentionally stored to support time-series price analysis
- Identical products scraped on different days produce multiple rows

This design enables:
- Price trend analysis
- Deal detection
- Cross-retailer comparisons

## Access & Authentication

This pipeline writes to a private Google BigQuery dataset and is not intended
to be executed by arbitrary users.

Authentication is handled via a Google Cloud service account with restricted
permissions. Credentials are intentionally not included in this repository.

Future plans include exposing read-only access via a public dashboard or
query interface without granting write access to the underlying warehouse.

## Testing & Reliability

Core transformation and enrichment logic is unit-tested using pytest.
Tests focus on deterministic product ID generation, attribute extraction,
schema alignment, and basic data quality constraints.
