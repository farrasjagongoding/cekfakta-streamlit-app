import streamlit as st
from newsapi import NewsApiClient # <-- Menggunakan NewsAPI
import time

# Impor fungsi yang kita butuhkan dari "kotak alat"
try:
    from utils import (
        proses_google # <-- Menggunakan 'proses_google' yang baru
    )
except ImportError:
    st.error("Gagal memuat modul 'utils.py'. Pastikan file tersebut ada di folder utama C:\\cek_fakta")
    st.stop()

# --- KONFIGURASI API ---
# PENTING: Kita akan baca dari 'Secrets' Streamlit Cloud
try:
    NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
except KeyError:
    st.error("API Key untuk NewsAPI belum diatur! (Cek 'Manage app' > 'Secrets')")
    st.stop()
# ------------------------

# Inisialisasi News API
try:
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
except Exception as e:
    st.error(f"Gagal menginisialisasi News API. Apakah API Key sudah benar? Error: {e}")
    st.stop()

st.header("Berita Terbaru & Referensi Cek Fakta")
st.markdown("Cari berita terbaru di Indonesia dan lihat apakah sudah ada verifikasi fakta terkait.")
st.markdown("---")

st.subheader("Cari Berita Teratas di Indonesia")
keyword = st.text_input("Masukkan kata kunci (opsional) atau biarkan kosong untuk berita teratas:")

if st.button("Cari Berita", type="primary"):
    
    with st.spinner(f"Mencari berita teratas dari Indonesia..."):
        try:
            # --- INI ADALAH ENDPOINT YANG BENAR ---
            all_articles = newsapi.get_top_headlines(
                q=keyword,
                country='id', # <-- Ini didukung oleh 'get_top_headlines'
                page_size=10
            )
            # -----------------------------------
        except Exception as e:
            # Ini akan menangkap jika API key Anda salah
            st.error(f"Error mengambil data dari NewsAPI: {e}")
            st.warning("Pastikan API Key Anda sudah benar di 'Secrets' (Manage app).")
            st.stop()

        if keyword:
            st.subheader(f"Hasil Pencarian untuk: '{keyword}'")
        else:
            st.subheader("Berita Teratas Indonesia Saat Ini")
        
        if not all_articles['articles']:
            st.error("Tidak ada artikel yang ditemukan.")
        
        for article in all_articles['articles']:
            title = article['title']
            source = article['source']['name']
            url = article['url']
            
            with st.expander(f"**{title}** (Sumber: {source})"):
                description = article.get('description', 'Tidak ada deskripsi.')
                if not description:
                    description = "Tidak ada deskripsi."

                st.markdown(f"**Ringkasan:** {description}")
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