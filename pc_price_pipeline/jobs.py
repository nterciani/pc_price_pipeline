import dagster as dg

daily_etl_job = dg.define_asset_job(
    name="daily_etl_job",
    selection=dg.AssetSelection.all()
)
