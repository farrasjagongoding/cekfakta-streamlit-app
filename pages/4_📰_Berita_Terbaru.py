@st.cache_data(ttl=600)
def get_google_news(keyword=""):
    """
    Mengambil berita Google News yang kompatibel dengan Streamlit Cloud.
    Hanya menggunakan hl=id (bahasa).
    """
    base_url = "https://news.google.com/rss"

    if keyword.strip():
        # Berita berdasarkan keyword
        url = f"{base_url}/search?q={keyword}&hl=id&num=20"
    else:
        # Berita utama
        url = f"{base_url}?hl=id&num=20"

    try:
        feed = feedparser.parse(url)
        return feed.entries
    except Exception as e:
        st.error(f"Error mengambil data dari Google News RSS: {e}")
        return []
