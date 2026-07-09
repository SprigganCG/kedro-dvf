"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.19.12

Refactored to use dynamic year-based pipeline generation.
"""

from kedro.pipeline import Pipeline, pipeline, node
from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings

from .nodes import import_raw_data, reduce_dimensions, filter_entries, stack_dvf, aggregate_data


def create_pipeline(**kwargs) -> Pipeline:
    """Dynamically create pipeline nodes for each year in parameters."""
    # Load years from parameters
    loader = OmegaConfigLoader(conf_source=settings.CONF_SOURCE)
    params = loader["parameters"]
    years = params.get("years", [2020, 2021, 2022, 2023, 2024, 2025])
    
    # Generate nodes for each year
    all_nodes = []
    for year in years:
        # Create year-specific nodes
        all_nodes.extend([
            node(
                func=import_raw_data,
                inputs=f"raw-dvf-{year}",
                outputs=f"int-imported-dvf.{year}",
                name=f"import_raw_data_{year}",
            ),
            node(
                func=reduce_dimensions,
                inputs=f"int-imported-dvf.{year}",
                outputs=f"int-reduced-dvf.{year}",
                name=f"reduce_dimensions_{year}",
            ),
            node(
                func=filter_entries,
                inputs=f"int-reduced-dvf.{year}",
                outputs=f"int-filtered-dvf.{year}",
                name=f"filter_entries_{year}",
            ),
        ])
    
    # Add stacking and aggregation nodes
    all_nodes.extend([
        node(
            func=stack_dvf,
            inputs=[f"int-filtered-dvf.{year}" for year in years],
            outputs="int-stacked-dvf",
            name="stack_all_years",
        ),
        node(
            func=aggregate_data,
            inputs="int-stacked-dvf",
            outputs=["int-aggregated-houses-dvf", "int-aggregated-flats-dvf"],
            name="aggregate_data"
        ),
    ])
    
    return pipeline(all_nodes)
