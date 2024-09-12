"""Create plots for the indicators."""
from pathlib import Path
from typing import List

import pandas as pd
import plotly.express as px
from settings import DATA_PATH
from console import console
import numpy as np
from plotly.subplots import make_subplots


def visualize_model(df_data, model_id) -> List:
    """Visualize single model.

    Returns figure.
    """
    console.rule(f"Visualize: {model_id}")
    # console.print(df_data)

    keys = ["Model", "Model metadata", "Archive", "Archive metadata"]
    # fig = make_subplots(
    #     rows=1, cols=4,
    #     column_titles=keys,
    #     specs=[[{"type": "polar"}, {"type": "polar"}, {"type": "polar"}, {"type": "polar"}]]
    # )

    figs = []
    dfs = [df_data[df_data["Type"] == key] for key in keys]
    for k, df in enumerate(dfs):
        key = keys[k]
        # fig.add_barpolar(
        #     df,
        #     r=df["Assessment"],
        #     theta=df["Short"],  # fillcolor=df_polar["Category"],
        #     # template="plotly_dark",
        #     opacity=0.9,
        #     row=1, col=k+1
        # )

        #fig.add_barpolar(df_polar, r="r", theta="ID", color="Category",
        #                 template="plotly_dark", row=1, col=2)
        fig = px.bar_polar(
            df, r="Assessment", theta="Short",
            color="Category",
            hover_name="ID",
            hover_data=["Indicator", "Category", "Priority"], # "Description", "Priority"
            color_discrete_sequence=[
                '#1f77b4',  # muted blue
                '#ff7f0e',  # safety orange
                '#2ca02c',  # cooked asparagus green
                '#d62728',  # brick red
                '#9467bd',  # muted purple
                '#8c564b',  # chestnut brown
                '#e377c2',  # raspberry yogurt pink
                '#7f7f7f',  # middle gray
                '#bcbd22',  # curry yellow-green
                '#17becf'  # blue-teal
            ]
            # template="plotly_dark"
        )
        fig.update_layout(
            title=key,
            showlegend=True,
            # xaxis=dict(
            #     tickmode='array',
            #     tickvals=[0, 0.5, 1],
            #     ticktext=['NA/0', '0.5', '1']
            # )
        )
        # fig.update_polars(radialaxis_dtick=[0, 0.5, 1])
        fig.update_polars(
            # radialraxis_tickmode="array",
            radialaxis_tickvals=[0, 0.5, 1],
            angularaxis_showgrid=True,
        )
        figs.append(fig)


    return figs, keys


if __name__ == "__main__":
    df_models = pd.read_csv(DATA_PATH / "models.csv")
    df_indicators = pd.read_csv(DATA_PATH / "indicators.csv")

    model_id = "BioModels_curated"
    df = pd.read_csv(DATA_PATH / f"{model_id}.csv")
    figs, keys = visualize_model(df, model_id=model_id)
    figs[0].show()
