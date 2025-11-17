import streamlit as st
import feedparser
import time

# Import fungsi dari utils
try:
    from utils import proses_google
except ImportError:
    st.error("Gagal memuat modul utils.py. Pastikan file tersimpan di folder C:\\cek_fakta")
    st.stop()

# ==========================
#   DAFTAR RSS INDONESIA
# ==========================
# Ini adalah daftar yang SUDAH SEIMBANG (1 feed per portal)
RSS_SOURCES = [
    # 1. CNN Indonesia (Nasional)
    "https://www.cnnindonesia.com/nasional/rss",

    # 2. Detik (News - Berita Utama)
    "https://rss.detik.com/index.php/detiknews",

    # 3. Kompas (Nasional)
    "https://news.kompas.com/rss/nasional",

    # 4. Tempo (Nasional)
    "https://rss.tempo.co/nasional",

    # 5. Viva (Berita Utama)
    "https://www.viva.co.id/rss/berita-utama.rss",

    # 6. Liputan6 (Berita Terbaru)
    "https://feed.liputan6.com/news",

    # 7. Okezone (Berita Utama)
    "https://sindikasi.okezone.com/index.php/rss/0/0/all",

    # 8. JawaPos (Berita Utama)
    "https://www.jawapos.com/rss",

    # 9. Antara News (Berita Terkini)
    "https://www.antaranews.com/rss/terkini",
    
    # 10. Tribunnews (Berita Utama)
    "https://www.tribunnews.com/rss"
]


# ==============================================
#   FUNGSI PENGAMBILAN BERITA MULTI PORTAL
# ==============================================
@st.cache_data(ttl=600) # Cache hasil selama 10 menit
def get_news(keyword=""):
    all_articles = []

    for url in RSS_SOURCES:
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries:
                title = entry.title if "title" in entry else "Tanpa Judul"
                link = entry.link if "link" in entry else "#"
                source = entry.get("source", {}).get("title", url)

                # Filter berdasarkan keyword jika ada
                if keyword:
                    if keyword.lower() in title.lower():
                        all_articles.append({
                            "title": title,
                            "link": link,
                            "published": entry.get("published", "Tidak diketahui"),
                            "source": source
                        })
                else:
                    # Jika tidak ada keyword, tambahkan semua
                    all_articles.append({
                        "title": title,
                        "link": link,
                        "published": entry.get("published", "Tidak diketahui"),
                        "source": source
                    })

        except Exception:
            pass  # Jika 1 RSS gagal fetch, lanjutkan

    return all_articles


# ======================
#     UI TAMPILAN
# ======================
st.header("Berita Terbaru dari Berbagai Portal Indonesia")
st.markdown("Cari berita terbaru dari berbagai platform nasional dan cek apakah sudah ada verifikasi faktanya.")
st.markdown("---")

st.subheader("Cari Berita di Indonesia")
keyword = st.text_input("Masukkan kata kunci (opsional). Biarkan kosong untuk semua berita:")

if st.button("Cari Berita", type="primary"):

    with st.spinner("Mengambil berita terbaru dari berbagai portal Indonesia..."):
        articles = get_news(keyword)

    if keyword:
        st.subheader(f"Hasil Pencarian untuk: '{keyword}'")
    else:
        st.subheader("Berita Terbaru dari Semua Portal")

    if not articles:
        st.error("Tidak ada artikel yang ditemukan.")
    else:
        # Batasi 20 berita teratas untuk jaga performa
        for article in articles[:20]:
            title = article["title"]
            source = article["source"]
            url = article["link"]
            published = article["published"]

            with st.expander(f"📰 {title} — *{source}*"):
                st.markdown(f"**Tanggal:** {published}")
                st.markdown(f"[Baca artikel asli]({url})", unsafe_allow_html=True)

                # Cek Fact Check
                with st.spinner("Mengecek Google Fact Check..."):
                    time.sleep(0.5)
                    hasil = proses_google(title)

                if hasil == "HOAKS":
                    st.error("⚠️ Berita ini terverifikasi **HOAKS** menurut Google Fact Check.")
                elif hasil == "FAKTA":
                    st.success("✔️ Berita ini terverifikasi **FAKTA** menurut Google Fact Check.")
                else:
                    st.info("ℹ️ Belum ada verifikasi fakta untuk judul berita ini.")

else:
    st.info("Masukkan kata kunci atau langsung klik tombol 'Cari Berita'.")
    
st.markdown("---")

if st.button("Kembali ke Halaman Utama"):
    st.switch_page("Home.py")