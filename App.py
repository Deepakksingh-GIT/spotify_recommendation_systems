import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -------------------- PAGE CONFIG -------------------- #
st.set_page_config(page_title="Spotify Dashboard", layout="wide")
st.title("🎵 Spotify Data Dashboard")

# -------------------- LOAD DATA -------------------- #
@st.cache_data
def load_data():
    try:
        if os.path.exists("spotify.csv"):
            df = pd.read_csv("spotify.csv")
        elif os.path.exists("spotify.xls"):
            df = pd.read_excel("spotify.xls")
        else:
            st.error("❌ No dataset file found (spotify.csv or spotify.xls)")
            st.stop()

        # Clean column names
        df.columns = df.columns.str.strip().str.lower()
        return df

    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

df = load_data()

# -------------------- REQUIRED COLUMNS CHECK -------------------- #
required_cols = ["artist", "popularity", "danceability", "energy"]

missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    st.error(f"❌ Required column(s) {missing_cols} not found in dataset!")
    st.write("### Available columns:")
    st.write(list(df.columns))
    st.stop()

# -------------------- SIDEBAR FILTER -------------------- #
st.sidebar.header("Filter Options")

artist = st.sidebar.multiselect(
    "Select Artist",
    options=sorted(df["artist"].unique()),
    default=sorted(df["artist"].unique())
)

df_filtered = df[df["artist"].isin(artist)]

# -------------------- KPI SECTION -------------------- #
st.markdown("## 📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Songs", len(df_filtered))
col2.metric("Total Artists", df_filtered["artist"].nunique())
col3.metric("Avg Popularity", round(df_filtered["popularity"].mean(), 2))
col4.metric("Avg Danceability", round(df_filtered["danceability"].mean(), 2))

st.markdown("---")

# -------------------- CHARTS -------------------- #
col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(
        df_filtered.groupby("artist")["popularity"].mean().reset_index(),
        x="artist",
        y="popularity",
        title="Average Popularity by Artist",
        color="artist"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.scatter(
        df_filtered,
        x="danceability",
        y="energy",
        color="artist",
        size="popularity",
        title="Danceability vs Energy"
    )
    st.plotly_chart(fig2, use_container_width=True)

# -------------------- DATA PREVIEW -------------------- #
st.markdown("### 📂 Dataset Preview")
st.dataframe(df_filtered)
