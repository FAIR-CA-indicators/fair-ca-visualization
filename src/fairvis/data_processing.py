"""Scripts for data processing."""
from pathlib import Path
from typing import List, Dict

import pandas as pd
from fairvis.console import console


def load_indicators(xlsx_path: Path) -> Dict[str, pd.DataFrame]:
    """Load the indicator data."""
    dfs = pd.read_excel(xlsx_path, sheet_name=None)

    # check that all models are listed in the models table
    df_indicators = dfs["indicators"]
    indicator_ids = {v for v in df_indicators.ID.values}
    df_indicators.set_index("ID", inplace=True)
    console.rule("Indicators", style="white")
    console.print(df_indicators)
    console.rule("Models", style="white")
    df_models = dfs["models"]
    console.print(df_models)
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


if __name__ == "__main__":
    from settings import DATA_PATH
    xlsx_path: Path = DATA_PATH / "FAIR_model_indicators_mkoenig.xlsx"
    dfs: Dict[str, pd.DataFrame] = load_indicators(xlsx_path)
    for model_id, df in dfs.items():
        df.to_csv(xlsx_path.parent / f"{model_id}.csv")
