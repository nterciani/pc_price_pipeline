import dagster as dg

daily_etl_job = dg.define_asset_job(
    name="daily_etl_job",
    selection=dg.AssetSelection.all(),
    executor_def=dg.multiprocess_executor.configured({
        "max_concurrent": 1,
    }),
)
