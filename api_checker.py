import streamlit as st
import requests

# ----------------------------------------------------
# PENTING: Ganti dengan API Key Google Fact Check Anda
API_KEY = st.secrets["GOOGLE_FACT_CHECK_KEY"]
# ----------------------------------------------------

API_ENDPOINT = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

def check_google_fact_check(query_text):
    """
    Mengirim kueri ke Google Fact Check API dan mengembalikan hasilnya.
    """
    
    params = {
        'query': query_text,
        'key': API_KEY,
        'languageCode': 'id'
    }

    try:
        response = requests.get(API_ENDPOINT, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'claims' in data and data['claims']:
                return data['claims'] # Sukses: Ditemukan klaim
            else:
                return None # Sukses: Tidak ditemukan klaim
        else:
            print(f"Error dari Google API: {response.status_code}")
            return None # Gagal

    except Exception as e:
        print(f"Terjadi error saat menghubungi API: {e}")
        return None # Gagal