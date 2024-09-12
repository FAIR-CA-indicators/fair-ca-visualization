"""Example to test visualization."""

import pandas as pd
from settings import DATA_PATH
from visualization import visualize_polar_barplots, visualize_barplot
from data_io import load_assessment


if __name__ == '__main__':

    df_models = pd.read_csv(DATA_PATH / "models.csv")
    df_indicators = pd.read_csv(DATA_PATH / "indicators.csv")

    model_id = "BioModels_curated"
    df = load_assessment(DATA_PATH / "assessments" / f"{model_id}.xlsx")

    # barplot
    fig = visualize_barplot(df)
    fig.show()

    # polar barplots
    # figs, keys = visualize_polar_barplots(df)
    # figs[0].show()
