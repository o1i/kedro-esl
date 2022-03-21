"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline

from esl.pipelines import c03_prostate_processing as pdp, c03_prostate_ds as pds


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    prostate_processing = pdp.create_pipeline()
    prostate_ds = pds.create_pipeline()
    

    return {
        "__default__": prostate_processing + prostate_ds,
        "pdp": prostate_processing,
        "pds": prostate_ds
        }
