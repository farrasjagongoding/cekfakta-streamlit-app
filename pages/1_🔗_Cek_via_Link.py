import streamlit as st
from urllib.parse import urlparse # Diperlukan untuk Analisis Domain

# Impor fungsi PROSESOR baru kita
try:
    from utils import (
        proses_mafindo,
        proses_google,
        proses_ai_lokal,
        proses_red_flags,
        buat_kesimpulan, # <-- OTAK KE-6 (Kesimpulan)
        scrape_article_text
    )
except ImportError:
    st.error("Gagal memuat modul 'utils.py' versi baru. Pastikan file sudah diperbarui.")
    st.stop()

# --- DAFTAR PUTIH (Bisa Anda tambahkan sendiri) ---
MEDIA_TERPERCAYA = [
    'kompas.com', 'detik.com', 'tempo.co', 'liputan6.com',
    'tirto.id', 'kumparan.com', 'antaranews.com', 'cnnindonesia.com',
    'cnbcindonesia.com', 'merdeka.com', 'okezone.com', 'sindonews.com',
    'suara.com', 'jawapos.com', 'pikiran-rakyat.com', 'viva.co.id',
    'tribunnews.com', 'thejakartapost.com'
]
# --------------------------------------------------

st.header("Analisis Link Artikel")
st.markdown("---")

url = st.text_input("Masukkan URL artikel:")

if st.button("Analisis Link", key="btn_link"):
    if url:
        st.divider()
        
        # --- KUMPULKAN SINYAL 1 (DOMAIN) ---
        hasil_domain = "NETRAL" # Default
        try:
            domain_bersih = urlparse(url).netloc.replace('www.', '')
            if domain_bersih in MEDIA_TERPERCAYA:
                hasil_domain = "TERPERCAYA"
            else:
                hasil_domain = "TIDAK DIKENAL"
        except Exception:
            hasil_domain = "ERROR" # Jika URL tidak valid
        
        # --- KUMPULKAN SINYAL 2, 3, 4 ---
        with st.spinner(f"Menganalisis Sinyal (Domain, Google, AI, Red Flags)..."):
            # Scrape Teks
            text_content, title = scrape_article_text(url)
            
            if not text_content or not title:
                st.error("Gagal mengambil artikel. Situs mungkin memblokir kami.")
                st.stop()
            
            st.success(f"Berhasil mengambil artikel: **{title}**")
            full_text = f"Judul: {title}\n\nIsi: {text_content}"
            
            # Sinyal 2: MAFINDO
            hasil_mafindo = proses_mafindo(title)
            
            # Sinyal 3: Google
            hasil_google = proses_google(title)
            
            # Sinyal 4: IndoBERT
            hasil_ai = proses_ai_lokal(full_text)
            
            # Sinyal 5: Red Flags
            hasil_red_flags = proses_red_flags(full_text)
        
        st.success("Analisis 5 Sinyal Selesai.")
        st.divider()
        
        # --- TAMPILKAN HASIL KESIMPULAN (OTAK KE-6) ---
        buat_kesimpulan(hasil_mafindo, hasil_google, hasil_ai, hasil_domain, hasil_red_flags)
        
        # --- TAMPILKAN DETAIL JIKA PERLU ---
        with st.expander("Lihat Detail Analisis 5 Sinyal"):
            st.subheader("Detail Sinyal:")
            st.write(f"1. Domain: `{hasil_domain}` ({domain_bersih})")
            st.write(f"2. MAFINDO: `{hasil_mafindo}`")
            st.write(f"3. Google: `{hasil_google}`")
            st.write(f"4. IndoBERT: `{hasil_ai[0]}` (Skor: {hasil_ai[1]*100:.2f}%)")
            st.write(f"5. Red Flags: Ditemukan `{hasil_red_flags[0]}` tanda bahaya.")
            if hasil_red_flags[0] > 0:
                st.write(f"   - {', '.join(hasil_red_flags[1])}")
            
    else:
        st.warning("Silakan masukkan URL")