"""Scripts for data processing."""
from pathlib import Path
import pandas as pd
from fairvis.console import console


def load_indicators(xlsx_path: Path) -> None:
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
    df = df_indicators.copy()
    for k, model_id in enumerate(model_ids):
        df_model = dfs[model_id]
        del df_model["Comment"]
        df_model.set_index("ID", inplace=True)
        df_model.rename(columns={"Assessment": model_id}, inplace=True)
        console.rule(model_id, align="left", style="blue")
        console.print(df_model)
        df = pd.merge(left=df, right=df_model, on="ID")

    console.print(df)
    return df



if __name__ == "__main__":
    from fairvis import DATA_PATH
    xlsx_path: Path = DATA_PATH / "FAIR_model_indicators_mkoenig.xlsx"
    df: pd.DataFrame = load_indicators(xlsx_path)
    df.to_csv(xlsx_path.parent / f"{xlsx_path.stem}.csv")
