"""Create plots for the indicators."""
from pathlib import Path

import pandas as pd
import plotly.express as px
from fairvis import DATA_PATH
from fairvis.console import console
import numpy as np
from plotly.subplots import make_subplots

def create_df_polar(df, model_id) -> pd.DataFrame:
    """Creates polar dataframe for visualization."""
    # https://plotly.com/python-api-reference/generated/plotly.express.bar_polar.html
    df_polar = df[["ID", "Category", model_id]]
    df_polar.rename(columns={model_id: "assessment"}, inplace=True)
    n_indicators = len(df_polar)

    # add polar coordinates for direction (calculate from number of indicators)
    theta_part = 360*n_indicators/(n_indicators+1)
    df_polar["theta"] = np.linspace(start=0, stop=360, num=n_indicators)
    # radial position (calculate from assessment)
    df_polar["r"] = df_polar["assessment"]
    # df_polar["r"] = np.linspace(start=0, stop=n_indicators-1, num=n_indicators)
    # get different colors
    df_polar["color"] = "tab:blue"
    console.print(df_polar)
    return df_polar


def visualize_model(df, model_id):
    """Visualize single model"""
    # TODO: split into archive and model categories
    # TODO: title of page

    console.rule(f"Visualize: {model_id}")
    df_polar = create_df_polar(df, model_id)

    # multiple subplot;
    # df = px.data.wind()
    # fig = px.bar_polar(df, r="frequency", theta="direction",
    #                   color="strength", template="plotly_dark",
    #                   color_discrete_sequence=px.colors.sequential.Plasma_r)
    # FIXME: add titles and column titles
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "polar"}, {"type": "polar"}]])
    # necessary to set the polar plots
    # FIXME: add hover information
    fig.add_barpolar(df_polar, r=df_polar["r"], theta=df_polar["ID"], #color=df_polar["Category"],
                       # template="plotly_dark",
                     row=1, col=1)
    fig.add_barpolar(df_polar, r=df_polar["r"], theta=df_polar["ID"],
                     # color=df_polar["Category"],
                     # template="plotly_dark",
                     row=1, col=2)
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
    csv_path: Path = DATA_PATH / "FAIR_model_indicators_mkoenig.csv"
    df = pd.read_csv(csv_path)
    console.print(df)
    model_ids = [c for c in df.columns if c not in {'ID', 'Category', 'Subcategory', 'Priority', 'Indicator', 'Description',
       'Assessment details'}]
    console.print(model_ids)

    visualize_model(df, model_ids[0])
