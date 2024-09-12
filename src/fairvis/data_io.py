"""Scripts for data IO, processing and validation."""
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import numpy as np
import pandas as pd
from settings import DATA_PATH, TEMPLATE_PATH
from console import console


def _load_indicators(xlsx_path: Path) -> Dict[str, pd.DataFrame]:
    """Load the indicator data."""
    dfs = pd.read_excel(xlsx_path, sheet_name=None)

    # check that all models are listed in the models table
    df_indicators = dfs["indicators"]
    indicator_ids = {v for v in df_indicators.ID.values}
    df_indicators.set_index("ID", inplace=True)
    console.rule("Indicators", style="white")
    # console.print(df_indicators)
    console.rule("Models", style="white")
    df_models = dfs["models"]
    # console.print(df_models)
    model_ids_def = {id for id in df_models.ID.values}

    df_indicators.to_csv(xlsx_path.parent / f"indicators.csv")
    df_models.to_csv(xlsx_path.parent / f"models.csv")

    # check the model sheet.
    model_ids = [k for k in dfs.keys() if k not in ["indicators", "models"]]
    for model_id in model_ids:
        if model_id not in model_ids_def:
            raise ValueError(f"model_id '{model_id}' not in ids")

    # check that indicators exists
    for model_id in model_ids:
        console.rule(model_id, align="left", style="blue")
        valid = True
        df_model = dfs[model_id]
        for indicator in df_model.ID.values:
            if indicator not in indicator_ids:
                console.print("Indicator incorrect", style="red")
                valid = False
        console.print(f"Model is valid: {valid}")

    # merge model sheets on the indicators
    dfs_out: Dict[str, pd.DataFrame] = {}
    for k, model_id in enumerate(model_ids):
        df = df_indicators.copy()
        df_model = dfs[model_id]
        # del df_model["Comment"]
        df_model.set_index("ID", inplace=True)
        # df_model.rename(columns={"Assessment": model_id}, inplace=True)
        console.rule(model_id, align="left", style="blue")
        console.print(df_model)
        df = pd.merge(left=df, right=df_model, on="ID")
        dfs_out[model_id] = df
        console.print(df)

    return dfs_out


def load_model_assessments() -> Dict[str, pd.DataFrame]:
    """Load all model assessment."""
    assessment_dir: Path = DATA_PATH / "assessments"
    df_dict: Dict[str, pd.DataFrame] = {}
    for f_xlsx in assessment_dir.glob("*.xlsx"):
        model_id = f_xlsx.stem
        df = load_assessment(f_xlsx)
        df_dict[model_id] = df

    return df_dict


def load_indicators(df_models: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """"""
    df_indicators = pd.read_excel(TEMPLATE_PATH, sheet_name=0)

    df_indicators.set_index("ID", inplace=True)
    del df_indicators["Description"]
    del df_indicators["Assessment details"]
    del df_indicators["Assessment"]
    del df_indicators["Comment"]

    assessments = [[0.0, 0.0, 0.0, 0.0] for _ in range(len(df_indicators))]
    for model_id, df_model in df_models.items():

        # Count classes
        for k, value in enumerate(df_model["Assessment"].values):
            # console.print(f"{value}, {type(value)}")
            if np.isnan(value):
                k_class = 0
            elif value == 0.0:
                k_class = 1
            elif value == 0.5:
                k_class = 2
            elif value == 1.0:
                k_class = 3

            assessments[k][k_class] = assessments[k][k_class] + 1.0

    # add assessment to indicators
    df_indicators["Assessment"] = assessments
    # console.print(df_indicators)

    return df_indicators


def load_assessment(xlsx_path: Path) -> pd.DataFrame:
    """Load assessment from file."""
    df = pd.read_excel(xlsx_path, sheet_name=0)
    df.set_index("ID", inplace=True)
    del df["Description"]
    del df["Assessment details"]
    # del df["Comment"]
    validate_assessment(df=df)

    return df


def validate_assessment(df: pd.DataFrame) -> None:
    """Validate assessment."""
    # load indicators from template and assert that everything exists;
    pass


if __name__ == "__main__":
    from settings import DATA_PATH

    # deprecated
    # xlsx_path: Path = DATA_PATH / "FAIR_model_indicators_mkoenig.xlsx"
    # dfs: Dict[str, pd.DataFrame] = _load_indicators(xlsx_path)

    df_models = load_model_assessments()
    # for model_id, df in df_models.items():
    #     console.rule(model_id, align="left", style="blue")
    #     console.print(df)

    df_indicator = load_indicators(df_models)
    console.rule("Indicators", align="left", style="red")
    console.print(df_indicator)
