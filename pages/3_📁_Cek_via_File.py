import streamlit as st

# Impor fungsi PROSESOR baru kita
try:
    from utils import (
        proses_mafindo,
        proses_google,
        proses_ai_lokal,
        proses_red_flags,
        buat_kesimpulan, # <-- OTAK KE-6 (Kesimpulan)
        read_pdf, 
        read_docx, 
        read_image_ocr
    )
except ImportError:
    st.error("Gagal memuat modul 'utils.py' versi baru. Pastikan file sudah diperbarui.")
    st.stop()

st.header("Analisis File Berita")
st.markdown("---")

claim_from_file = st.text_input("Masukkan Judul/Klaim dari file (opsional):", key="claim_file")
uploaded_file = st.file_uploader("Upload file (.txt, .pdf, .docx, .png, .jpg)", 
                                 type=["txt", "pdf", "docx", "png", "jpg"])

extracted_text = ""
if uploaded_file is not None:
    # 1. Ekstrak Teks dari File
    with st.spinner("Membaca file..."):
        if uploaded_file.type == "text/plain":
            extracted_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            extracted_text = read_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            extracted_text = read_docx(uploaded_file)
        elif uploaded_file.type in ["image/png", "image/jpeg"]:
            extracted_text = read_image_ocr(uploaded_file)
    
    st.text_area("Teks yang berhasil diekstrak:", extracted_text, height=150)

if st.button("Analisis File", key="btn_file"):
    if not extracted_text:
        st.error("File belum di-upload atau tidak ada teks yang bisa diekstrak.")
    else:
        st.divider() 
        full_text = f"Judul: {claim_from_file}\n\nIsi: {extracted_text}"
        query_for_api = claim_from_file if claim_from_file else extracted_text[:150] 
        
        # --- KUMPULKAN SEMUA SINYAL (TANPA MENAMPILKAN) ---
        
        with st.spinner("Menganalisis Sinyal (MAFINDO, Google, AI, Red Flags)..."):
            # Sinyal 1: MAFINDO (Netral, Hoaks)
            hasil_mafindo = proses_mafindo(query_for_api)
            
            # Sinyal 2: Google (Netral, Hoaks, Fakta)
            hasil_google = proses_google(query_for_api)
            
            # Sinyal 3: IndoBERT (Label, Skor)
            hasil_ai = proses_ai_lokal(full_text)
            
            # Sinyal 4: Red Flags (Jumlah, Daftar)
            hasil_red_flags = proses_red_flags(full_text)
            
            # Sinyal 5: Domain (Untuk 'Cek File', domain selalu NETRAL)
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