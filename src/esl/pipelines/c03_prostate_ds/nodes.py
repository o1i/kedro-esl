"""
This is a boilerplate pipeline 'c03_prostate_ds'
generated using Kedro 0.17.7
"""
from typing import Tuple

import numpy as np
from numpy.linalg import solve
import pandas as pd
from scipy.linalg import qr
from scipy.stats import t
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
from statsmodels.api import OLS
from statsmodels.regression.linear_model import RegressionResultsWrapper
from tabulate import tabulate


def fit_x_standardiser(df: pd.DataFrame, params: dict):
    model = StandardScaler(with_mean=params["location"], with_std=params["scale"])
    model.fit(df)
    return [model]


def fit_linear_regression(df: pd.DataFrame, y: pd.Series, params: dict) -> OLS:
    used = sm.add_constant(df) if params["intercept"] else df
    model = sm.OLS(y, used)
    fit = model.fit()
    return [fit]


def standardise_x(std: StandardScaler, df: pd.DataFrame) -> pd.DataFrame:
    return [pd.DataFrame(std.transform(df), columns = df.columns)]


def produce_metrics(fit: RegressionResultsWrapper) -> dict:
    outputs = fit.params.to_dict()
    summary = repr(fit.summary())
    return outputs, summary

def manual_regression(df: pd.DataFrame, y: pd.Series, params: dict) -> str:
    # https://pages.stat.wisc.edu/~larget/math496/qr.html
    used = sm.add_constant(df) if params["intercept"] else df
    n = len(used)
    p = used.values.shape[1]
    Q, R = qr(used.values)
    coefs = solve(R[:p, :], np.matmul(Q.T, y.values)[:p]).reshape([-1])
    pred = np.matmul(used.values, coefs).reshape([-1])
    resid = y.values.reshape([-1]) - pred
    sig2_hat = np.matmul(resid.T, resid) / (n - p)
    std_err = np.sqrt(np.diag(np.linalg.inv(np.matmul(R[:p, :].T, R[:p, :]))) * sig2_hat)
    T = coefs / std_err
    P = 2*(1-t.cdf(np.abs(T), df = n - p))
    ql = t.ppf(0.025, df=n - p) * std_err + coefs
    qu = t.ppf(0.975, df=n - p) * std_err + coefs
    ols_summary = tabulate(pd.DataFrame({
        "coef": np.round(coefs, 4), 
        "std_err": np.round(std_err, 3), 
        "t": np.round(T, 3),
        "P>|t|": np.round(P, 3), 
        "[0.025": np.round(ql, 3), 
        "0.975]": np.round(qu, 3)
        }, index=used.columns), headers="keys")
    r2 = np.sum(np.square(pred - np.mean(pred))) / np.sum(np.square(y.values - np.mean(y.values)))
    r2a = 1 - (1-r2) * (n - 1) / (n - p)
    out = f"n: {n}\np + 1: {p}\nsig2_hat: {sig2_hat}\n\nR2: {r2}\nAdj R2: {r2a}\n\n{ols_summary}"
    return out


def save_hyperparams(params: dict) -> list:
    return [{**params["regression"], **params["scaler"]}]

