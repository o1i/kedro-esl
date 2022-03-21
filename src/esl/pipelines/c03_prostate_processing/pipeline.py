"""
This is a boilerplate pipeline 'c03_prostate_processing'
generated using Kedro 0.17.7
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import split_input, print_correlations


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=split_input,
            inputs=["prostate_raw"],
            outputs=["x_all", "y_all", "x_train", "y_train", "x_test", "y_test"],
            name="split_data",
        ),
        node(
            func=print_correlations,
            inputs=["x_all"],
            outputs=["corr_x_all"],
            name="corr_all",
        ),
        node(
            func=print_correlations,
            inputs=["x_train"],
            outputs=["corr_x_train"],
            name="corr_train",
        )
    ])
