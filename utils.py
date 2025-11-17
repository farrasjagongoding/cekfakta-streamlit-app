import streamlit as st
import time

# Impor semua "otak" dan "alat"
try:
    from api_checker import check_google_fact_check
    from mafindo_checker import check_mafindo_api
    from analyzer import analyze_with_indobert
    from scraper import scrape_article_text
    from file_parser import read_pdf, read_docx, read_image_ocr
except ImportError as e:
    st.error(f"FATAL ERROR: Gagal mengimpor modul.")
    st.error(f"Detail: {e}")    
    st.error("Pastikan semua file .py (api_checker.py, analyzer.py, dll) ada di folder C:\\cek_fakta")
    st.stop()

# --- FUNGSI-FUNGSI "PROSESOR" (BARU) ---
# Fungsi-fungsi ini MENGEMBALIKAN data, tidak menampilkan apa-apa.

def proses_mafindo(keyword):
    """Mengecek MAFINDO. Mengembalikan 'HOAKS', 'FAKTA', atau 'NETRAL'."""
    results = check_mafindo_api(keyword)
    if results:
        # Asumsi API MAFINDO hanya mengembalikan hoaks
        return "HOAKS"
    return "NETRAL" # Sesuai permintaan Anda, netral = 0

def proses_google(keyword):
    """Mengecek Google Fact Check. Mengembalikan 'HOAKS', 'FAKTA', atau 'NETRAL'."""
    results = check_google_fact_check(keyword)
    if results:
        rating = results[0]['claimReview'][0]['textualRating'].lower()
        if rating in ["palsu", "salah", "hoaks", "false"]:
            return "HOAKS"
        if rating in ["benar", "fakta", "true"]:
            return "FAKTA"
    return "NETRAL" # Sesuai permintaan Anda, netral = 0

def proses_ai_lokal(full_text):
    """Mengecek IndoBERT. Mengembalikan tuple (label, score), cth: ('Hoax', 0.95)"""
    results = analyze_with_indobert(full_text)
    if results:
        return results # Cth: ('Hoax', 0.95)
    return ("NETRAL", 0)

def proses_red_flags(full_text):
    """Mengecek Red Flags. Mengembalikan jumlah flags dan listnya, cth: (3, ['list', 'flags'])"""
    flags_ditemukan = []
    try:
        kapital = sum(1 for c in full_text if c.isupper())
        total = len(full_text)
        if total > 50 and (kapital / total) > 0.10: 
            flags_ditemukan.append("Penggunaan huruf kapital berlebihan")
    except Exception: pass
    if full_text.count('!') > 5:
        flags_ditemukan.append("Penggunaan tanda seru berlebihan")
    kata_pemicu = [
        'segera sebarkan', 'viralkan', 'waspada!!!', 
        'jangan berhenti di anda', 'bagikan info penting ini'
    ]
    for kata in kata_pemicu:
        if kata in full_text.lower():
            flags_ditemukan.append(f"Mengandung kata pemicu: '{kata}'")
    return (len(flags_ditemukan), flags_ditemukan) # Cth: (3, ['list', 'flags'])

# --- FUNGSI DISCLAIMER (BARU) ---
def tampilkan_disclaimer_mencurigakan():
    """Menampilkan peringatan agar pengguna mengecek ulang."""
    st.markdown("---")
    st.warning(
        "**💡 SARAN (CEK KEMBALI):**\n\n"
        "Hasil ini menunjukkan adanya **indikasi mencurigakan** (Hoaks, Netral, atau Red Flags).\n\n"
        "Alat AI tidak sempurna. Kami sangat menyarankan Anda untuk **membaca kembali isi teks/artikel secara kritis** dan membandingkannya dengan sumber berita terpercaya lainnya sebelum mempercayai atau menyebarkannya."
    )
# ------------------------------------

# --- FUNGSI KESIMPULAN (OTAK KE-6) - DIPERBARUI ---
def buat_kesimpulan(hasil_mafindo, hasil_google, hasil_ai, hasil_domain, hasil_red_flags):
    """
    Menganalisis semua sinyal dan memberikan kesimpulan akhir.
    """
    st.header("Kesimpulan Akhir", divider="red")

    # --- ATURAN 1: SINYAL TERKUAT (Game Over) ---
    if hasil_mafindo == "HOAKS":
        st.error("**KESIMPULAN: HAMPIR PASTI HOAKS**")
        st.write("Sinyal terkuat: Ditemukan di database TurnBackHoax.id (MAFINDO).")
        tampilkan_disclaimer_mencurigakan() # <-- DITAMBAHKAN
        return # Selesai
        
    if hasil_google == "HOAKS":
        st.error("**KESIMPULAN: SANGAT CENDERUNG HOAKS**")
        st.write("Sinyal terkuat: Ditemukan di database Google Fact Check dengan rating 'Palsu'.")
        tampilkan_disclaimer_mencurigakan() # <-- DITAMBAHKAN
        return # Selesai

    if hasil_google == "FAKTA":
        st.success("**KESIMPULAN: SANGAT CENDERUNG FAKTA**")
        st.write("Sinyal terkuat: Ditemukan di database Google Fact Check dengan rating 'Benar'.")
        # Tidak perlu disclaimer di sini
        return # Selesai

    # --- ATURAN 2: SINYAL NETRAL (Gunakan AI + Sinyal Lain) ---
    label_ai, skor_ai = hasil_ai
    jumlah_flags, _ = hasil_red_flags
    
    skor_akhir = 0
    
    if label_ai.lower() == "hoax":
        skor_akhir += (skor_ai * 60) # AI hoaks = +60 poin
    else:
        skor_akhir -= (skor_ai * 30) # AI fakta = -30 poin
        
    if hasil_domain == "TIDAK DIKENAL":
        skor_akhir += 20 # Domain tidak dikenal = +20 poin
        
    skor_akhir += (jumlah_flags * 10) # Tiap red flag = +10 poin
    
    if skor_akhir < -20: skor_akhir = -20
    if skor_akhir > 100: skor_akhir = 100

    # Tampilkan Kesimpulan berdasarkan Skor Akhir
    if skor_akhir >= 70:
        st.error(f"**KESIMPULAN: SANGAT CENDERUNG HOAKS (Skor Bahaya: {skor_akhir:.0f}/100)**")
        st.write("Alasan: Analisis AI (IndoBERT) mendeteksi pola hoaks yang kuat dan/atau ditemukan banyak 'Red Flags'.")
        tampilkan_disclaimer_mencurigakan() # <-- DITAMBAHKAN
    elif skor_akhir >= 30:
        st.warning(f"**KESIMPULAN: CENDERUNG HOAKS (Skor Bahaya: {skor_akhir:.0f}/100)**")
        st.write("Alasan: Ditemukan kombinasi antara pola AI, domain tidak dikenal, atau 'Red Flags'. Harap sangat berhati-hati.")
        tampilkan_disclaimer_mencurigakan() # <-- DITAMBAHKAN
    elif skor_akhir > 0:
        st.info(f"**KESIMPULAN: NETRAL (Skor Bahaya: {skor_akhir:.0f}/100)**")
        st.write("Alasan: Tidak ada sinyal kuat yang ditemukan, namun AI juga tidak yakin ini fakta. Anggap saja netral.")
        tampilkan_disclaimer_mencurigakan() # <-- DITAMBAHKAN
    else:
        st.success(f"**KESIMPULAN: CENDERUNG FAKTA (Skor Bahaya: {skor_akhir:.0f}/100)**")
        st.write("Alasan: AI (IndoBERT) mendeteksi pola bahasa yang valid dan minim 'Red Flags'.")
        # Tidak perlu disclaimer di sini