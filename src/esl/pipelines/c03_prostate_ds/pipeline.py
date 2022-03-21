"""
This is a boilerplate pipeline 'c03_prostate_ds'
generated using Kedro 0.17.7
"""

from kedro.config import ConfigLoader
from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    fit_x_standardiser, standardise_x, fit_linear_regression, 
    print_linear_regression, save_hyperparams
)


conf_paths = ["conf/base", "conf/local"]
conf_loader = ConfigLoader(conf_paths)
parameters = conf_loader.get("parameters*", "parameters*/**")


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=fit_x_standardiser,
            inputs=["x_train", "params:scaler"],
            outputs=["x_standardiser"],
            name="fit_x_standardiser",
        ),
        node(
            func=standardise_x,
            inputs=["x_standardiser", "x_train"],
            outputs=["x_train_std"],
            name="standardise_x_train",
        ),
        node(
            func=standardise_x,
            inputs=["x_standardiser", "x_test"],
            outputs=["x_test_std"],
            name="standardise_x_test",
        ),
        node(
            func=fit_linear_regression,
            inputs=["x_train_std", "y_train", "params:regression"],
            outputs=["linear_model"],
            name="fit_linear_model",
        ),
        node(
            func=print_linear_regression,
            inputs=["linear_model"],
            outputs=["linear_model_fit", "metrics"],
            name="print_linear_regression",
        ),
        node(
            func=save_hyperparams,
            inputs=["parameters"],
            outputs=["hyperparameters"],
            name="save_hparams",
        ),

    ])
