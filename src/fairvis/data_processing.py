"""Scripts for data processing."""
from pathlib import Path
import pandas as pd
from fairvis.console import console


def load_indicators(xlsx_path: Path) -> None:
    """Load the indicator data."""
    dfs = pd.read_excel(xlsx_path, sheet_name=None)

    # check that all models are listed in the models table
    df_indicators = dfs["indicators"]
    console.rule("Indicators", style="white")
    console.print(df_indicators)
    console.rule("Models", style="white")
    df_models = dfs["models"]
    console.print(df_models)
    model_ids_def = {id for id in df_models.ID.values}

    # check the model sheet.
    model_ids = [k for k in dfs.keys() if k not in ["indicators", "models"]]
    for model_id in model_ids:
        if model_id not in model_ids_def:
            raise ValueError(f"model_id '{model_id}' not in ids")

    # merge model sheets on the indicators
    df = df_indicators.copy()
    for model_id in model_ids:
        df_model = dfs[model_id]
        del df_model["Comment"]
        df = pd.merge(df, df_model, on=["ID"])

    console.print(df)



if __name__ == "__main__":
    from fairvis import DATA_PATH
    xlsx_path: Path = DATA_PATH / "FAIR_model_indicators_mkoenig.xlsx"
    load_indicators(xlsx_path)
