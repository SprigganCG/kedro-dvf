"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.19.12
"""

from kedro.pipeline import Pipeline, pipeline,node

from .nodes import import_raw_data,reduce_dimensions,filter_entries,stack_dvf,aggregate_data

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
        # manage 2023
        node(
            func=import_raw_data,
            inputs="raw-dvf-2023",
            outputs="int-imported-dvf.2023",
            name="import_raw_data_2023",
        ),
        node(
            func=reduce_dimensions,
            inputs="int-imported-dvf.2023",
            outputs="int-reduced-dvf.2023",
            name="reduce_dimensions_2023",
        ),
        node(
            func=filter_entries,
            inputs="int-reduced-dvf.2023",
            outputs="int-filtered-dvf.2023",
            name="filter_entries_2023",
        ),
        # manage 2022
        node(
            func=import_raw_data,
            inputs="raw-dvf-2022",
            outputs="int-imported-dvf.2022",
            name="import_raw_data_2022",
        ),
        node(
            func=reduce_dimensions,
            inputs="int-imported-dvf.2022",
            outputs="int-reduced-dvf.2022",
            name="reduce_dimensions_2022",
        ),
        node(
            func=filter_entries,
            inputs="int-reduced-dvf.2022",
            outputs="int-filtered-dvf.2022",
            name="filter_entries_2022",
        ),
        # manage 2021
        node(
            func=import_raw_data,
            inputs="raw-dvf-2021",
            outputs="int-imported-dvf.2021",
            name="import_raw_data_2021",
        ),
        node(
            func=reduce_dimensions,
            inputs="int-imported-dvf.2021",
            outputs="int-reduced-dvf.2021",
            name="reduce_dimensions_2021",
        ),
        node(
            func=filter_entries,
            inputs="int-reduced-dvf.2021",
            outputs="int-filtered-dvf.2021",
            name="filter_entries_2021",
        ),
        # manage 2020
        node(
            func=import_raw_data,
            inputs="raw-dvf-2020",
            outputs="int-imported-dvf.2020",
            name="import_raw_data_2020",
        ),
        node(
            func=reduce_dimensions,
            inputs="int-imported-dvf.2020",
            outputs="int-reduced-dvf.2020",
            name="reduce_dimensions_2020",
        ),
        node(
            func=filter_entries,
            inputs="int-reduced-dvf.2020",
            outputs="int-filtered-dvf.2020",
            name="filter_entries_2020",
        ),
        # stack all the years
        node(
            func=stack_dvf,
            inputs=["int-filtered-dvf.2024",
                    "int-filtered-dvf.2023",
                    "int-filtered-dvf.2022",
                    "int-filtered-dvf.2021",
                    "int-filtered-dvf.2020"],
            outputs="int-stacked-dvf",
            name="stack_all_years",
        ),
        # aggregate data
        node(
            func=aggregate_data,
            inputs="int-stacked-dvf",
            outputs=["int-aggregated-houses-dvf","int-aggregated-flats-dvf"],
            name="aggregate_data"),
    ])
