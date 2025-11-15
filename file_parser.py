import streamlit as st
import PyPDF2
from docx import Document
from PIL import Image
import pytesseract

# --- Fungsi Bantuan untuk Membaca File ---

def read_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error membaca PDF: {e}")
        return None

def read_docx(file):
    try:
        doc = Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error membaca DOCX: {e}")
        return None

def read_image_ocr(file):
    try:
        image = Image.open(file)
        # Pastikan bahasa 'ind' (Indonesia) sudah ter-install di Tesseract Anda
        text = pytesseract.image_to_string(image, lang='ind') 
        return text
    except pytesseract.TesseractNotFoundError:
        st.error("TESSERACT TIDAK DITEMUKAN. Apakah Anda sudah meng-install Tesseract-OCR?")
        st.info("Download di: https://github.com/tesseract-ocr/tesseract/wiki")
        return None
    except Exception as e:
        st.error(f"Error melakukan OCR: {e}")
        return None