from dagster import Definitions, load_assets_from_package_module

from . import assets  # noqa: TID252
from .jobs import daily_etl_job

all_assets = load_assets_from_package_module(assets)
all_jobs = [daily_etl_job]

defs = Definitions(
    assets=all_assets,
    jobs=all_jobs,
)
