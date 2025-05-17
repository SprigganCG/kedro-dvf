"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.19.12
"""

from kedro.pipeline import Pipeline, pipeline,node

from .nodes import import_raw_data,reduce_dimensions,filter_entries

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        # manage 2024
        node(
            func=import_raw_data,
            inputs="raw-dvf-2024",
            outputs="int-imported-dvf.2024",
            name="import_raw_data_2024",
        ),
        node(
            func=reduce_dimensions,
            inputs="int-imported-dvf.2024",
            outputs="int-reduced-dvf.2024",
            name="reduce_dimensions_2024",
        ),
        node(
            func=filter_entries,
            inputs="int-reduced-dvf.2024",
            outputs="int-filtered-dvf.2024",
            name="filter_entries_2024",
        ),

        ])
