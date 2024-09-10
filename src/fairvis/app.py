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
tab_about, tab_indicators, tab_models = st.tabs(["About", "Indicators", "Models"])

with tab_about:
    st.markdown(
        """
        # FAIR COMBINE Archive Indicators
        ## Goals
        - Achieve Community-consensus on FAIR indicators
        - Develop FAIR evaluation guidelines
        - Implement a FAIR evaluation tool

        ## Reference
        **Optimising research through FAIRification of computational models in biology**.

        Irina Balaur1, David Nickerson2, Danielle Welter1, Judith A.H. Wodke3, Francois Ancien1, Tom Gebhardt3, Valentin Grouès1, Henning Hermjakob4, Matthias König5, Nicole Radde6, Adrien Rougny1, Reinhard Schneider1, Rahuman Sheriff4, Kirubel Biruk Shiferaw3, Melanie Stefan7, Venkata Satagopam1, Dagmar Waltemath3

        1 Luxembourg Centre for Systems Biomedicine (LCSB), University of Luxembourg, Luxembourg
        2 Auckland Bioengineering Institute, University of Auckland, New Zealand
        3 Medical Informatics Laboratory, University Medicine Greifswald, Germany
        4 European Molecular Biology Laboratory, European Bioinformatics Institute (EMBL-EBI), UK
        5 Institute for Biology, Institute for Theoretical Biology, Humboldt University of Berlin, Germany
        6 Institute for Stochastics and Applications, University Stuttgart, Germany
        7 Medical School Berlin, Berlin, Germany
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
    fig = visualize_model(df_data=df_model, model_id=model_id)
    st.plotly_chart(fig)

    # show dataframe

    st.dataframe(df_model, use_container_width=True)


# row = df[df.sim_key == simulation_id]
# visualize_model(df, model_id=model_id)

# st.markdown(f"**simulation**: `{simulation_id}`, **pattern**: `{row.pattern_name.values[0]}`, **substrate flow**: `Sv{row.boundary_flow_key.values[0]}`")
#
# # video rendering
# url = f"https://github.com/matthiaskoenig/spt-app/raw/main/data/{simulation_id}_h264.mp4"
# video_placeholder = st.empty()
# video_html = f"""
#     <video width="80%" controls="false" autoplay loop="true" align="middle">
#       <source src="{url}" type="video/mp4" />
#       Your browser does not support the video tag.
#     </video>
# """
# video_placeholder.empty()
# time.sleep(1.0)
# video_placeholder.markdown(video_html, unsafe_allow_html=True)
# st.divider()
#
# # image
# def render_img_html(image_b64):
#     st.markdown(f"<img style='max-width: 80%;max-height: 100%;' src='data:image/png;base64, {image_b64}'/>", unsafe_allow_html=True)
#
# def image_to_base64(image_path):
#     image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
#     _, encoded_image = cv2.imencode(".png", image)
#     base64_image = base64.b64encode(encoded_image.tobytes()).decode("utf-8")
#     return base64_image
#
#
# image_path = data_path / f"{simulation_id}.png"
# render_img_html(image_to_base64(str(image_path)))
