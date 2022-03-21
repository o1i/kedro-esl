"""
This is a boilerplate pipeline 'c03_prostate_ds'
generated using Kedro 0.17.7
"""
from typing import Tuple

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


def fit_x_standardiser(df: pd.DataFrame, params: dict):
    model = StandardScaler(with_mean=params["location"], with_std=params["scale"])
    model.fit(df)
    return [model]


def fit_linear_regression(df: pd.DataFrame, y: pd.Series, params: dict) -> LinearRegression:
    model = LinearRegression(fit_intercept=params["intercept"])
    model.fit(df, y)
    return [model]


def standardise_x(std: StandardScaler, df: pd.DataFrame) -> pd.DataFrame:
    return [pd.DataFrame(std.transform(df), columns = df.columns)]


def print_linear_regression(model: LinearRegression) -> Tuple[pd.DataFrame, dict]:
    df = pd.concat([
        pd.DataFrame({"variable": ["intercept"], "coef": model.intercept_}),
        pd.DataFrame({"variable": model.feature_names_in_, "coef": model.coef_[0]}),
    ], axis=0, ignore_index=True)

    return [df, df.set_index("variable")["coef"].to_dict()]


def save_hyperparams(params: dict) -> list:
    return [{**params["regression"], **params["scaler"]}]