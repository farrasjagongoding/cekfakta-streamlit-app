# C:\cek_fakta\mafindo_checker.py
# VERSI PERBAIKAN (Bisa 'skip' jika API Key kosong)

import requests
import streamlit as st

# --- KONFIGURASI API MAFINDO (YUDISTIRA) ---
API_KEY = st.secrets["MAFINDO_API_KEY"]

API_ENDPOINT = "https://yudistira.turnbackhoax.id/api/antihoax/search" 
# ----------------------------------------------------

def check_mafindo_api(keyword):
    """
    Mengirim kueri ke MAFINDO (TurnBackHoax.id) API.
    """
    
    # --- PERBAIKAN DI SINI ---
    # Jika API key masih placeholder, jangan jalankan API.
    # Ini mencegah error selagi Anda menunggu persetujuan.
    if API_KEY == "https://yudistira.turnbackhoax.id/api/":
        print("API Key MAFINDO belum diisi. Melewatkan pengecekan MAFINDO.")
        return None
    # ---------------------------
    
    data_to_send = {
        'q': keyword
    }
    
    # Header ini mungkin perlu diubah sesuai dokumentasi
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    try:
        response = requests.post(API_ENDPOINT, json=data_to_send, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            # 'news' adalah tebakan, cek dokumentasi untuk format balasan
            if data and data.get('news'):
                return data['news'] 
            else:
                return None 
        else:
            print(f"Error dari MAFINDO API: {response.status_code} - {response.text}")
            st.error(f"Error MAFINDO API: {response.status_code}. Mungkin API Key salah?")
            return None 

    except Exception as e:
        print(f"Terjadi error saat menghubungi MAFINDO API: {e}")
        return None