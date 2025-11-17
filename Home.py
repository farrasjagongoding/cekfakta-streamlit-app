import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="CekFakta",
    page_icon="🛡️",
    layout="wide"
)

# --- 2. CSS KUSTOM (DENGAN FONT & PENYEMBUNYI SIDEBAR) ---
hide_streamlit_style = """
            <style>
            /* --- 1. IMPORT FONT DARI GOOGLE --- */
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Roboto:wght@400;700&display=swap');

            /* --- 2. SEMBUNYIKAN ELEMEN STREAMLIT --- */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            [data-testid="stSidebar"] {
                display: none;
            }

            /* --- 3. FONT GLOBAL --- */
            html, body, [class*="st-"] {
                font-family: 'Roboto', sans-serif; /* Font default adalah Roboto */
            }

            /* --- HERO SECTION --- */
            .hero-container {
                padding: 4rem 2rem;
                padding-bottom: 5rem; 
                background-image: linear-gradient(135deg, #007bff 0%, #6610f2 100%);
                color: white;
                border-radius: 15px;
                text-align: center;
                margin-bottom: 0; 
                box-shadow: 0 10px 30px rgba(0, 123, 255, 0.3);
            }
            .hero-title {
                font-family: 'Montserrat', sans-serif; 
                font-weight: 800;
                font-size: 4.5rem;
                margin-bottom: 0.75rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }
            .hero-subtitle {
                font-family: 'Roboto', sans-serif;
                font-size: 1.8rem;
                color: rgba(255, 255, 255, 0.9);
                margin-bottom: 2.5rem;
            }

            /* --- PERBAIKAN TOMBOL HERO (INI YANG ANDA INGINKAN) --- */
            
            /* 1. Container untuk menarik tombol ke atas */
            .hero-button-container {
                margin-top: -3.5rem; 
                margin-bottom: 3rem; 
                /* text-align: center; (Ini tidak kita butuhkan jika pakai columns) */
                position: relative; 
                z-index: 10;
            }

            /* 2. Style tombol agar putih (seperti yang diminta) */
            /* Kita targetkan tombol di dalam 'col2' (kolom tengah) */
            .hero-button-container [data-testid="stHorizontalBlock"] [data-testid="stButton"] button {
                font-family: 'Montserrat', sans-serif;
                border: 2px solid white;
                border-radius: 30px;
                background-color: transparent; /* Transparan */
                color: white; /* Teks putih */
                padding: 0.8rem 2.5rem;
                font-size: 1.1rem;
                font-weight: 700;
                transition: all 0.3s ease-in-out;
            }
            
            /* 3. Style hover (seperti yang diminta) */
            .hero-button-container [data-testid="stHorizontalBlock"] [data-testid="stButton"] button:hover {
                background-color: white;
                color: #007bff; /* Teks biru saat hover */
                transform: translateY(-3px);
                box-shadow: 0 5px 15px rgba(255,255,255,0.3);
            }
            /* -------------------------------------------------- */


            /* --- HEADER --- */
            h1[data-testid="stHeader"] {
                font-family: 'Montserrat', sans-serif;
                color: #007bff;
                font-weight: 700;
            }
            
            /* --- KOTAK FITUR (Tidak berubah) --- */
            .feature-box {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 12px;
                padding: 30px 20px;
                box-shadow: 0 6px 20px rgba(0,0,0,0.08);
                transition: all 0.3s ease;
                height: 320px; 
                text-align: center;
                display: flex;
                flex-direction: column;
                justify-content: space-between; 
            }
            .feature-box:hover {
                box-shadow: 0 12px 35px rgba(0,0,0,0.15);
                transform: translateY(-8px);
            }
            .feature-box .feature-icon {
                font-size: 4rem;
                margin-bottom: 0.5rem;
            }
            .feature-box h3 {
                font-family: 'Montserrat', sans-serif;
                color: #343a40;
                margin-top: 0.5rem;
                margin-bottom: 0.75rem;
            }
            .feature-box .stButton button {
                background-color: #007bff;
                color: white;
                font-weight: 600;
            }

            /* --- FOOTER --- */
            .footer {
                text-align: center;
                padding: 2.5rem 0;
                color: #555;
                font-size: 0.9rem;
                background-color: #f0f2f6;
                margin-top: 3rem;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 3. BAGIAN ATAS (HERO SECTION) ---
st.markdown(
    """
    <div class="hero-container">
        <h1 class='hero-title'>CEK FAKTA</h1>
        <p class='hero-subtitle'>Berpikir Kritis, Cek Dulu Faktanya. Perisai Anda Melawan Disinformasi.</p>
        </div>
    """,
    unsafe_allow_html=True
)

# --- TOMBOL NAVIGASI HERO (FUNGSIONAL) ---
st.markdown('<div class="hero-button-container">', unsafe_allow_html=True)

# KEMBALIKAN st.columns UNTUK MENENGKAHKAN TOMBOL
col1, col2, col3 = st.columns([2, 3, 2]) # Rasio 2:3:2 (seperti kode Anda sebelumnya)
with col2:
    if st.button(
        "Kumpulan Berita Terverifikasi",
        key="hero_button",
        use_container_width=True # Tombol akan mengisi kolom tengah (col2)
    ):
        # Arahkan ke halaman News API yang kita buat
        st.switch_page("pages/4_📰_Berita_Terbaru.py")
    
st.markdown('</div>', unsafe_allow_html=True)
# ---------------------------------

st.write("") # Spasi
st.write("") # Spasi

# --- 4. BAGIAN FITUR (DENGAN TOMBOL NAVIGASI) ---
st.header("Layanan Kami", divider="blue")
st.write("")

col1_fitur, col2_fitur, col3_fitur = st.columns(3, gap="large")

with col1_fitur:
    st.markdown(
        """
        <div class="feature-box">
            <div> <span class="feature-icon">🔗</span>
                <h3>Cek via Link</h3>
                <p>Punya link artikel meragukan? Kami akan menganalisis sumber, konten, dan membandingkannya dengan database hoaks terverifikasi.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Pilih Fitur 🔗", key="btn_link", use_container_width=True):
        st.switch_page("pages/1_🔗_Cek_via_Link.py")

with col2_fitur:
    st.markdown(
        """
        <div class="feature-box">
            <div> <span class="feature-icon">✍️</span>
                <h3>Cek via Teks</h3>
                <p>Menerima pesan berantai di WhatsApp? Salin (copy-paste) teksnya ke sini, dan biarkan AI kami menganalisis pola bahasa dan klaimnya secara mendalam.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Pilih Fitur ✍️", key="btn_teks", use_container_width=True):
        st.switch_page("pages/2_✍️_Cek_via_Teks.py")


with col3_fitur:
    st.markdown(
        """
        <div class="feature-box">
            <div> <span class="feature-icon">📁</span>
                <h3>Cek via File</h3>
                <p>Dapat kiriman file PDF, .docx, atau gambar (screenshot)? Upload filenya dan kami akan mengekstrak serta menganalisis isinya untuk Anda.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Pilih Fitur 📁", key="btn_file", use_container_width=True):
        st.switch_page("pages/3_📁_Cek_via_File.py")

st.write("") # Spasi
st.write("") # Spasi

# --- 5. BAGIAN PENUTUP  ---
st.header("Mengapa Verifikasi Penting?", divider="blue")
st.write("")

left_col, right_col = st.columns([2, 1], gap="large")

with left_col:
    st.markdown(
        """
        ### Jangan Jadi Bagian dari Rantai Hoaks
        
        Hoaks dan disinformasi dirancang untuk memanipulasi emosi dan nalar kita. 
        Mereka bisa merusak reputasi, memicu kepanikan, dan memecah belah masyarakat. 
        Setiap kali Anda memverifikasi sebuah informasi sebelum membagikannya, 
        Anda tidak hanya melindungi diri sendiri, tetapi juga berkontribusi 
        membangun ekosistem digital Indonesia yang lebih sehat dan cerdas.
        """
    )
    
with right_col:
    st.info(
        "**Status Proyek:**\n\n"
        "Aplikasi CekFakta.id sedang dalam tahap pengembangan aktif. "
        "Beberapa fitur masih belum berfungsi dengan baik, Karena website ini masih dalam tahap pengembangan"
    )

st.write("") # Spasi
st.write("") # Spasi

# --- 6. FOOTER ---
st.markdown(
    """
    <div class="footer">
        © 2025 Cek Fakta
    </div>
    """,
    unsafe_allow_html=True
)