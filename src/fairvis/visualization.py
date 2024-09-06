"""Create plots for the indicators."""
from pathlib import Path

import pandas as pd
import plotly.express as px
from settings import DATA_PATH
from console import console
import numpy as np
from plotly.subplots import make_subplots


def visualize_model(df_data, model_id):
    """Visualize single model"""
    console.rule(f"Visualize: {model_id}")
    console.print(df_data)

    keys = ["Model", "Model metadata", "Archive", "Archive metadata"]
    fig = make_subplots(
        rows=1, cols=4,
        column_titles=keys,
        specs=[[{"type": "polar"}, {"type": "polar"}, {"type": "polar"}, {"type": "polar"}]]
    )
    # FIXME: add hover information
    # FIXME: add color


    dfs = [df_data[df_data["Type"] == key] for key in keys]
    for k, df in enumerate(dfs):
        fig.add_barpolar(
            df,
            r=df["Assessment"],
            theta=df["Short"],  # fillcolor=df_polar["Category"],
            # template="plotly_dark",
            opacity=0.9,
            row=1, col=k+1
        )

    #fig.add_barpolar(df_polar, r="r", theta="ID", color="Category",
    #                 template="plotly_dark", row=1, col=2)
    # fig = px.bar_polar(df_polar, r="r", theta="ID", color="Category",
    #                    template="plotly_dark")
    fig.update_layout(
        title=model_id,
        showlegend=True
    )
    fig.show()


if __name__ == "__main__":
    df_models = pd.read_csv(DATA_PATH / "models.csv")
    df_indicators = pd.read_csv(DATA_PATH / "indicators.csv")

    model_id = "BioModels_curated"
    df = pd.read_csv(DATA_PATH / f"{model_id}.csv")
    visualize_model(df, model_id=model_id)
