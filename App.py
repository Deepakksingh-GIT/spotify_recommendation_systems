import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Spotify Recommendation Dashboard",
    layout="wide",
    page_icon="🎵"
)

# ---------------- CUSTOM STYLING ---------------- #
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1, h2, h3 {
    color: #1DB954;
}
.stMetric {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

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

# Remove unwanted columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df.columns = df.columns.astype(str)

# ---------------- KPIs ---------------- #
st.markdown("## 📊 Key Insights")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🎵 Total Songs", df.shape[1])
col2.metric("👥 Total Users / Rows", df.shape[0])
col3.metric("📊 Total Data Points", df.size)
col4.metric("📈 Avg Similarity Score", round(df.mean().mean(), 4))

st.markdown("---")

# ---------------- SEARCH + SLIDER ---------------- #
st.markdown("## 🎧 Get Song Recommendations")

search_song = st.text_input("🔍 Search Song")

song_list = list(df.columns)

# Filter song list by search
if search_song:
    filtered_songs = [song for song in song_list if search_song.lower() in song.lower()]
else:
    filtered_songs = song_list

selected_song = st.selectbox("Select Song", filtered_songs)

top_n = st.slider("⭐ Select Top N Recommendations", 5, 20, 10)

# ---------------- RECOMMENDATION LOGIC ---------------- #
if selected_song:

    similarity_scores = (
        df[selected_song]
        .sort_values(ascending=False)
        .head(top_n)
    )

    st.markdown(f"### 🔥 Top {top_n} Recommendations for: {selected_song}")

    # -------- BAR CHART -------- #
    fig_bar = px.bar(
        similarity_scores,
        x=similarity_scores.index,
        y=similarity_scores.values,
        title="Similarity Scores",
        labels={"x": "Song", "y": "Similarity Score"},
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # -------- TABLE -------- #
    st.dataframe(similarity_scores)

    st.markdown("---")

    # -------- HEATMAP -------- #
    st.markdown("### 📊 Similarity Heatmap")

    heatmap_data = df[similarity_scores.index].corr()

    fig_heatmap = px.imshow(
        heatmap_data,
        text_auto=True,
        aspect="auto",
        title="Song Similarity Heatmap"
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

# ---------------- DATA PREVIEW ---------------- #
st.markdown("### 📂 Dataset Preview")
st.dataframe(df)
