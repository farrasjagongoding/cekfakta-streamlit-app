import streamlit as st

# Impor fungsi PROSESOR baru kita
try:
    from utils import (
        proses_mafindo,
        proses_google,
        proses_ai_lokal,
        proses_red_flags,
        buat_kesimpulan # <-- OTAK KE-6 (Kesimpulan)
    )
except ImportError:
    st.error("Gagal memuat modul 'utils.py' versi baru. Pastikan file sudah diperbarui.")
    st.stop()

st.header("Analisis Teks Berita")
st.markdown("---")

claim_to_check = st.text_input("Masukkan Judul atau Klaim Utama:")
text_to_check = st.text_area("Salin dan tempel isi berita di sini:", height=200)

if st.button("Analisis Teks", key="btn_teks"):
    if claim_to_check and text_to_check:
        st.divider() 
        full_text = f"Judul: {claim_to_check}\n\nIsi: {text_to_check}"
        
        # --- KUMPULKAN SEMUA SINYAL (TANPA MENAMPILKAN) ---
        
        with st.spinner("Menganalisis Sinyal (MAFINDO, Google, AI, Red Flags)..."):
            # Sinyal 1: MAFINDO (Netral, Hoaks)
            hasil_mafindo = proses_mafindo(claim_to_check)
            
            # Sinyal 2: Google (Netral, Hoaks, Fakta)
            hasil_google = proses_google(claim_to_check)
            
            # Sinyal 3: IndoBERT (Label, Skor)
            hasil_ai = proses_ai_lokal(full_text)
            
            # Sinyal 4: Red Flags (Jumlah, Daftar)
            hasil_red_flags = proses_red_flags(full_text)
            
            # Sinyal 5: Domain (Untuk 'Cek Teks', domain selalu NETRAL)
            hasil_domain = "NETRAL" 
        
        st.success("Analisis 4 Sinyal Selesai.")
        st.divider()
        
        # --- TAMPILKAN HASIL KESIMPULAN (OTAK KE-6) ---
        buat_kesimpulan(hasil_mafindo, hasil_google, hasil_ai, hasil_domain, hasil_red_flags)
        
        # --- TAMPILKAN DETAIL JIKA PERLU ---
        with st.expander("Lihat Detail Analisis 4 Sinyal"):
            st.subheader("Detail Sinyal:")
            st.write(f"1. MAFINDO: `{hasil_mafindo}`")
            st.write(f"2. Google: `{hasil_google}`")
            st.write(f"3. IndoBERT: `{hasil_ai[0]}` (Skor: {hasil_ai[1]*100:.2f}%)")
            st.write(f"4. Red Flags: Ditemukan `{hasil_red_flags[0]}` tanda bahaya.")
            if hasil_red_flags[0] > 0:
                st.write(f"   - {', '.join(hasil_red_flags[1])}")
            
    else:
        st.warning("Silakan masukkan Judul/Klaim DAN Isi Teks untuk dianalisis.")