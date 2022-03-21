"""
This is a boilerplate pipeline 'c03_prostate_processing'
generated using Kedro 0.17.7
"""
import numpy as np
import pandas as pd
from tabulate import tabulate


def split_input(df: pd.DataFrame) -> tuple:
    X = df[["lcavol", "lweight", "age", "lbph", "svi", "lcp", "gleason", "pgg45"]]
    y = df["lpsa"]
    ind_train = df["train"] == "T"
    return X, y, X[ind_train], y[ind_train], X[~ind_train], y[~ind_train]


def print_correlations(df: pd.DataFrame) -> list:
    corr_matrix = pd.DataFrame(np.round(np.corrcoef(df.T), 3), columns = df.columns)
    return [tabulate(corr_matrix)]