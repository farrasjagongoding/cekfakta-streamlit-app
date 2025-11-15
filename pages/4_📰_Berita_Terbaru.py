# C:\cek_fakta\pages\4_📰_Berita_Terbaru.py
# VERSI BARU (Kompatibel dengan utils.py v3.1)
import streamlit as st
import feedparser 
import time

try:
    from utils import (
        proses_google # <-- Kita pakai 'proses_google' BUKAN 'tampilkan_hasil_google'
    )
except ImportError:
    st.error("Gagal memuat modul 'utils.py'. Pastikan file tersebut ada di folder utama C:\\cek_fakta")
    st.stop()

@st.cache_data(ttl=600) 
def get_google_news(keyword=""):
    base_url = "https://news.google.com/rss"
    if keyword:
        url = f"{base_url}/search?q={keyword}&gl=ID&hl=id&ceid=ID:id"
    else:
        url = f"{base_url}?gl=ID&hl=id&ceid=ID:id"
    try:
        feed = feedparser.parse(url)
        return feed.entries
    except Exception as e:
        st.error(f"Error mengambil data dari Google News RSS: {e}")
        return []

st.header("Berita Terbaru dari Google News Indonesia")
st.markdown("Cari berita terbaru di Indonesia dan lihat apakah sudah ada verifikasi fakta terkait.")
st.markdown("---")

st.subheader("Cari Berita Teratas di Indonesia")
keyword = st.text_input("Masukkan kata kunci (opsional) atau biarkan kosong untuk berita teratas:")

if st.button("Cari Berita", type="primary"):
    with st.spinner(f"Mencari berita teratas dari Indonesia..."):
        articles = get_google_news(keyword)

        if keyword:
            st.subheader(f"Hasil Pencarian untuk: '{keyword}'")
        else:
            st.subheader("Berita Teratas Indonesia Saat Ini")
        
        if not articles:
            st.error("Tidak ada artikel yang ditemukan.")
        
        for article in articles[:10]:
            title = article.title
            source = article.source.title
            url = article.link
            
            with st.expander(f"**{title}** (Sumber: {source})"):
                st.markdown(f"**Tanggal Terbit:** {article.get('published', 'Tidak diketahui')}")
                st.markdown(f"[Baca artikel asli]({url})", unsafe_allow_html=True)
                
                with st.spinner("Mengecek Google Fact Check untuk artikel ini..."):
                    time.sleep(0.5) 
                    hasil_google = proses_google(title) # Panggil fungsi PROSESOR
                
                if hasil_google == "HOAKS":
                    st.error("Ditemukan verifikasi: **HOAKS** (Berdasarkan database Google Fact Check).")
                elif hasil_google == "FAKTA":
                    st.success("Ditemukan verifikasi: **FAKTA** (Berdasarkan database Google Fact Check).")
                else:
                    st.success("Belum ada verifikasi fakta yang ditemukan di Google untuk judul ini.")
                        
else:
    st.info("Masukkan kata kunci (atau biarkan kosong) dan klik 'Cari Berita' untuk memulai.")

st.markdown("---")
if st.button("Kembali ke Halaman Utama"):
    st.switch_page("Home.py")