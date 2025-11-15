from transformers import pipeline
import streamlit as st

@st.cache_resource
def muat_model():
    print("MEMULAI DOWNLOAD MODEL INDOBERT... (Hanya sekali)")
    try:
        hoax_classifier = pipeline(
            "text-classification",
            model="Rifky/indobert-hoax-classification",
            tokenizer="indobenchmark/indobert-base-p1"
        )
        print("Model IndoBERT berhasil dimuat.")
        return hoax_classifier
    except Exception as e:
        st.error(f"Gagal memuat model IndoBERT. Pastikan Anda terkoneksi internet. Error: {e}")
        return None

def analyze_with_indobert(article_text):
    hoax_classifier = muat_model() 
    
    if hoax_classifier is None:
        return None # Kembalikan None jika model gagal

    try:
        teks_yang_dipotong = article_text[:2000]
        result = hoax_classifier(teks_yang_dipotong)
        
        label = result[0]['label'] # 'Hoax' or 'Valid'
        score = result[0]['score'] # 0.0 - 1.0
        
        # --- PERUBAHAN UTAMA ---
        # Kita kembalikan datanya, BUKAN teks
        return (label, score) 
        # -------------------------

    except Exception as e:
        print(f"Error saat menjalankan analisis: {e}")
        return None