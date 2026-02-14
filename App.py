import streamlit as st
import pandas as pd
import os

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="Spotify Recommendation Dashboard", layout="wide")
st.title("🎵 Spotify Recommendation Dashboard")

# ---------------- LOAD DATA ---------------- #
@st.cache_data
def load_data():
    try:
        if os.path.exists("spotify.csv"):
            df = pd.read_csv("spotify.csv")
        elif os.path.exists("spotify.xls"):
            df = pd.read_excel("spotify.xls")
        else:
            st.error("❌ No dataset found (spotify.csv or spotify.xls)")
            st.stop()

        return df

    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

df = load_data()

# ---------------- CLEAN DATA ---------------- #
# Remove unnamed index column if exists
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Convert all column names to string
df.columns = df.columns.astype(str)

# ---------------- KPIs ---------------- #
st.markdown("## 📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("Total Songs", df.shape[1])
col2.metric("Total Users / Rows", df.shape[0])
col3.metric("Total Data Points", df.size)

st.markdown("---")

# ---------------- SONG SELECTOR ---------------- #
st.markdown("## 🎧 Get Recommendations")

song_list = list(df.columns)

selected_song = st.selectbox(
    "Select a Song",
    song_list
)

# ---------------- RECOMMENDATION LOGIC ---------------- #
# Assuming matrix similarity structure
if selected_song:

    try:
        recommendations = (
            df[selected_song]
            .sort_values(ascending=False)
            .head(10)
        )

        st.markdown(f"### 🔥 Top Recommendations for: {selected_song}")

        st.table(recommendations)

    except Exception as e:
        st.error(f"Error generating recommendations: {e}")

# ---------------- DATA PREVIEW ---------------- #
st.markdown("### 📂 Dataset Preview")
st.dataframe(df)
