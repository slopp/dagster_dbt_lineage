from dagster import asset, Definitions, AssetExecutionContext, AssetKey
from dagster_dbt import dbt_assets, DbtCliResource
from seed import load_raw
from pathlib import Path

@asset(
    compute_kind = 'duckdb'
)
def my_source():
    """ A function that loads data into our database """
    load_raw()


DBT_PROJECT = "dbt_project"
MANIFEST = DBT_PROJECT + "/target/manifest.json"
dbt = DbtCliResource(project_dir=DBT_PROJECT)

# always re-genereate the manifest on project reload
dbt.cli(["--quiet", "parse"], target_path=Path("target")).wait()

from dagster_dbt import DagsterDbtTranslator

@dbt_assets(
    manifest=MANIFEST
)
def my_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    """ Function to create assets for dbt models """
    yield from dbt.cli(["build"], context=context).stream()


defs = Definitions(
    assets=[my_source, my_dbt_assets], 
    resources = {"dbt": dbt}
)