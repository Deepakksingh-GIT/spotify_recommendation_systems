import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="Spotify Dashboard", layout="wide")

# Title
st.title("🎵 Spotify Data Dashboard")

@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)

    if os.path.exists(os.path.join(base_path, "spotify.csv")):
        return pd.read_csv(os.path.join(base_path, "spotify.csv"))

    elif os.path.exists(os.path.join(base_path, "spotify.xls")):
        return pd.read_excel(os.path.join(base_path, "spotify.xls"))

    else:
        st.error("Dataset file not found!")
        st.stop()

df = load_data()


# Sidebar Filters
st.sidebar.header("Filter Options")

artist = st.sidebar.multiselect(
    "Select Artist",
    options=df["artist"].unique(),
    default=df["artist"].unique()
)

df_filtered = df[df["artist"].isin(artist)]

# ================= KPIs ================= #

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Songs", len(df_filtered))

with col2:
    st.metric("Total Artists", df_filtered["artist"].nunique())

with col3:
    st.metric("Avg Popularity", round(df_filtered["popularity"].mean(), 2))

with col4:
    st.metric("Avg Danceability", round(df_filtered["danceability"].mean(), 2))

st.markdown("---")

# ================= Charts ================= #

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        df_filtered.groupby("artist")["popularity"].mean().reset_index(),
        x="artist",
        y="popularity",
        title="Average Popularity by Artist"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.scatter(
        df_filtered,
        x="danceability",
        y="energy",
        color="artist",
        title="Danceability vs Energy"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Data Preview
st.markdown("### Dataset Preview")
st.dataframe(df_filtered)
