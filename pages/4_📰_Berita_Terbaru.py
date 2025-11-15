import streamlit as st
import feedparser
import time

# ================================
# IMPORT FUNGSI DARI UTILS
# ================================
try:
    from utils import proses_google
except ImportError:
    st.error("Gagal memuat modul 'utils.py'. Pastikan file tersebut berada di folder utama.")
    st.stop()

# ================================
# FUNGSI AMBIL BERITA GOOGLE NEWS
# ================================
@st.cache_data(ttl=600)
def get_google_news(keyword: str = ""):
    """
    Mengambil berita dari Google News Indonesia via RSS.
    Bebas API key. Aman di Streamlit Cloud.
    """
    base_url = "https://news.google.com/rss"

    # Gunakan bahasa Indonesia saja (hindari gl=ID karena bentrok IP)
    if keyword:
        url = f"{base_url}/search?q={keyword}&hl=id&ceid=ID:id"
    else:
        url = f"{base_url}?hl=id&ceid=ID:id"

    try:
        feed = feedparser.parse(url)

        # Jika RSS gagal parse, feed.entries akan kosong → aman
        return feed.entries
    except Exception as e:
        st.error(f"Gagal mengambil data dari Google News RSS: {e}")
        return []

# ================================
# UI / TAMPILAN
# ================================
st.header("Berita Terbaru dari Google News Indonesia")
st.markdown("Cari berita terbaru di Indonesia dan lihat apakah sudah ada verifikasi fakta terkait.")
st.markdown("---")

st.subheader("Cari Berita Teratas di Indonesia")
keyword = st.text_input("Masukkan kata kunci (opsional) atau biarkan kosong untuk berita teratas:")

if st.button("Cari Berita", type="primary"):

    with st.spinner("Mengambil berita..."):
        articles = get_google_news(keyword)

    # Judul Hasil
    if keyword:
        st.subheader(f"Hasil Pencarian untuk: **{keyword}**")
    else:
        st.subheader("Berita Teratas (Bahasa Indonesia)")

    # Tidak ada artikel ditemukan
    if not articles:
        st.error("Tidak ada artikel yang ditemukan.")
        st.stop()

    # Tampilkan 10 berita teratas
    for article in articles[:10]:
        title = article.title
        source = article.source.title if hasattr(article, "source") else "Tidak diketahui"
        link = article.link
        published = article.get("published", "Tidak diketahui")

        with st.expander(f"**{title}** — *{source}*"):
            st.markdown(f"**Tanggal Terbit:** {published}")
            st.markdown(f"[Baca Artikel Asli]({link})")

            # Fact Check Google
            with st.spinner("Mengecek Google Fact Check..."):
                time.sleep(0.5)
                hasil_google = proses_google(title)

            if hasil_google == "HOAKS":
                st.error("Ditemukan verifikasi: **HOAKS** (Google Fact Check).")
            elif hasil_google == "FAKTA":
                st.success("Ditemukan verifikasi: **FAKTA** (Google Fact Check).")
            else:
                st.info("Belum ada verifikasi fakta untuk artikel ini.")

else:
    st.info("Masukkan kata kunci lalu klik 'Cari Berita'.")

st.markdown("---")
if st.button("Kembali ke Halaman Utama"):
    st.switch_page("Home.py")
