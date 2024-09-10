from typing import Tuple, Dict

import pandas as pd
import streamlit as st
import numpy as np
from pathlib import Path
from settings import DATA_PATH
from console import console
from visualization import visualize_model

st.set_page_config(
    page_title="FAIR-CA-Indicators",
    page_icon="🧊",
    layout="wide",
    # initial_sidebar_state="expanded",
    menu_items={
        "Get help": "mailto:konigmatt@googlemail.com",
        "Report a bug": "https://github.com/FAIR-CA-indicators/fair-ca-visualization.git/issues/new",
        "About": """
        FAIR-CA-Indicators application.
        """,
    },
)
st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                    padding-bottom: 1rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

@st.cache_data
def load_data() -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """Load data."""
    df_models = pd.read_csv(DATA_PATH / "models.csv")
    df_indicators = pd.read_csv(DATA_PATH / "indicators.csv")
    df_indicators.set_index("ID", inplace=True)
    del df_indicators["Description"]
    del df_indicators["Assessment details"]

    assessments = [[0.0, 0.0, 0.0, 0.0] for _ in range(len(df_indicators))]
    models: Dict[str, pd.DataFrame] = {}
    for model_id in df_models.ID.values:
        df_model = pd.read_csv(DATA_PATH / f"{model_id}.csv")
        del df_model["Description"]
        del df_model["Assessment details"]
        del df_model["Comment"]
        models[model_id] = df_model

        # Count classes
        for k, value in enumerate(df_model["Assessment"].values):
            console.print(f"{value}, {type(value)}")
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
    console.print(df_indicators)

    return df_indicators, models


df_indicators, models = load_data()


# --- Main ----------------------------------------------------------------------------
st.markdown(
    """
    # FAIR COMBINE Archive Indicators
    """
)
tab_about, tab_models, tab_indicators, tab_assessment = st.tabs(["About", "Models", "Indicators", "Assess your Model"])

with tab_about:
    st.markdown(
        """
        Computational models are essential tools for studying complex systems which,
        particularly in clinical settings, need to be quality-approved and transparent.
        A community-driven approach to enhance the transparency and communication of
        model features is adherence to the principles of Findability, Accessibility,
        Interoperability and Reusability (FAIR). We propose here an adaptation of the
        FAIR indicators published by the Research Data Alliance to assess the
        FAIRness of models encoded in domain-specific standards, such as those
        established by [COMBINE](https://co.mbine.org).

        ## Example visualization
        The following demonstrates the Model and Model metadata indicators for the
        BioModels_C19_curated example. To browse the FAIR indicators for the example
        models select the **Models Tab** above.
        To browse the indicators select the **Indicators Tab** above.
        """
    )
    figs_example, _ = visualize_model(df_data=models["BioModels_C19_curated"],
                                      model_id=["BioModels_C19_curated"])
    col1a, col2a = st.columns(2)
    with col1a:
        st.plotly_chart(figs_example[0])
    with col2a:
        st.plotly_chart(figs_example[1])

    st.markdown(
        """
        ## Assess your model

        To assess your model select the **Assess your Model Tab**. We provide a
        template with instructions from https://github.com/FAIR-CA-indicators/fair-ca-visualization/raw/main/data/template.xlsx.
        """
    )
    st.html(
        """
        <h2>Reference</h2>
        <strong>Optimising research through FAIRification of computational models in biology</strong></br>

        Irina Balaur<sup>1</sup>, David Nickerson<sup>2</sup>, Danielle Welter<sup>1</sup>, Judith A.H. Wodke<sup>3</sup>, Francois Ancien<sup>1</sup>, Tom Gebhardt<sup>3</sup>, Valentin Grouès<sup>1</sup>, Henning Hermjakob<sup>4</sup>, Matthias König<sup>5</sup>, Nicole Radde<sup>6</sup>, Adrien Rougny<sup>1</sup>, Reinhard Schneider<sup>1</sup>, Rahuman Sheriff<sup>4</sup>, Kirubel Biruk Shiferaw<sup>3</sup>, Melanie Stefan<sup>7</sup>, Venkata Satagopam<sup>1</sup>, Dagmar Waltemath<sup>3</sup></br>

        <sup>1</sup> Luxembourg Centre for Systems Biomedicine (LCSB), University of Luxembourg, Luxembourg</br>
        <sup>2</sup> Auckland Bioengineering Institute, University of Auckland, New Zealand</br>
        <sup>3</sup> Medical Informatics Laboratory, University Medicine Greifswald, Germany</br>
        <sup>4</sup> European Molecular Biology Laboratory, European Bioinformatics Institute (EMBL-EBI), UK</br>
        <sup>5</sup> Institute for Biology, Institute for Theoretical Biology, Humboldt University of Berlin, Germany</br>
        <sup>6</sup> Institute for Stochastics and Applications, University Stuttgart, Germany</br>
        <sup>7</sup> Medical School Berlin, Berlin, Germany</br>

        <h2>Funding</h2>
        Matthias König was supported by the BMBF within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA).
        """
    )

with tab_indicators:
    st.dataframe(
        data=df_indicators,
        use_container_width=True,
        column_config={
            "Assessment": st.column_config.BarChartColumn(
                "FAIR Assessment",
                help="Assessment of all models (NA, 0.0, 0.5, 1.0)",
                # y_min=0,
                # y_max=1,
            ),
        },
    )


with tab_models:
    model_id = st.selectbox(
        "Select model",
        index=0,
        options=list(models.keys()),
    )
    df_model = models[model_id]

    # plotly plot
    figs, keys = visualize_model(df_data=df_model, model_id=model_id)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(figs[0])
    with col2:
        st.plotly_chart(figs[1])
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(figs[2])
    with col4:
        st.plotly_chart(figs[3])

    # show dataframe
    st.dataframe(df_model, use_container_width=True)

with tab_assessment:
    st.html(
        """
        The template for assessment is available here: <strong><a href="https://github.com/FAIR-CA-indicators/fair-ca-visualization/raw/main/data/FAIR_assessment_template.xlsx" target="_blank">FAIR_assessment_template.xlsx</a></strong>.

        Fill out the assessment column and upload the assessment below.
        """
    )
    st.file_uploader("Upload FAIR model assessment", type=None, accept_multiple_files=False, key=None, help=None,
                     on_change=None, args=None, kwargs=None, disabled=False,
                     label_visibility="visible")

st.divider()
st.markdown(
    """
    © 2024 Matthias König, https://github.com/FAIR-CA-indicators/fair-ca-visualization
    """
)
