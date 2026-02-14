import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ================= PAGE CONFIG ================= #
st.set_page_config(page_title="Spotify Dashboard", layout="wide")

st.title("🎵 Spotify Data Dashboard")

# ================= LOAD DATA ================= #

@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)

    csv_path = os.path.join(base_path, "spotify.csv")
    xls_path = os.path.join(base_path, "spotify.xls")

    try:
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        elif os.path.exists(xls_path):
            df = pd.read_excel(xls_path)
        else:
            st.error("Dataset file not found!")
            st.stop()

        if df.empty:
            st.error("Dataset file is empty!")
            st.stop()

        # Clean column names (VERY IMPORTANT)
        df.columns = df.columns.str.strip().str.lower()

        return df

    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        st.stop()


df = load_data()

# ================= REQUIRED COLUMN CHECK ================= #

required_columns = ["artist", "popularity", "danceability", "energy"]

for col in required_columns:
    if col not in df.columns:
        st.error(f"Required column '{col}' not found in dataset!")
        st.write("Available columns:", df.columns)
        st.stop()

# ================= SIDEBAR FILTER ================= #

st.sidebar.header("Filter Options")

artist = st.sidebar.multiselect(
    "Select Artist",
    options=sorted(df["artist"].dropna().unique()),
    default=sorted(df["artist"].dropna().unique())
)

df_filtered = df[df["artist"].isin(artist)]

# ================= KPIs ================= #

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Songs", len(df_filtered))

with col2:
    st.metric("Total Artists", df_filtered["artist"].nunique())

with col3:
    st.metric(
        "Avg Popularity",
        round(df_filtered["popularity"].mean(), 2)
    )

with col4:
    st.metric(
        "Avg Danceability",
        round(df_filtered["danceability"].mean(), 2)
    )

st.markdown("---")

# ================= CHARTS ================= #

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

# ================= DATA PREVIEW ================= #

st.markdown("### Dataset Preview")
st.dataframe(df_filtered)
