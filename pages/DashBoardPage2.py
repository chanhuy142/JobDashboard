#đếm sô luọng job theo từng loại bằng cấp
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import geopandas as gpd
st.set_page_config(
    page_title="Tình hình việc làm ở Việt Nam",
    page_icon="📊",
    
    layout="wide",
    )
alt.themes.enable("dark")
col = st.columns((0.7,1,1.7), gap='small')