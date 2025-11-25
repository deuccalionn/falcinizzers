import streamlit as st
import time
import random

# --- KÜTÜPHANE KONTROLÜ ---
try:
    from PIL import Image
    import google.generativeai as genai
    AI_AVAILABLE = True
except ImportError as e:
    st.error(f"KÜTÜPHANE EKSİK: requirements.txt dosyasını kontrol et! Hata: {e}")
    st.stop()

st.set_page_config(page_title="Mistik Falcı", page_icon="🔮", layout="wide")

# --- SABİTLER ---
CARD_BACK = "https://i.pinimg.com/originals/70/4f/2e/704f2e04eb58172c3426e959600994f3.jpg"
MUSIC_URL = "https://upload.wikimedia.org/wikipedia/commons/0/0b/Erik_Satie_-_Gnossienne_1.ogg"

# --- TASARIM ---
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at center, #1a0b2e 0%, #000000 100%); color: #fff; }
    h1 { color: #FFD700 !important; font-family: 'Georgia', serif; text-align: center; }
    .mystic-card { background: rgba(255,255,255,0.1); border: 1px solid #FFD700; border-radius: 15px; padding: 20px; margin-top: 20px; text-align: center; color: #eee; }
    .stButton>button { background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%); color: white; border-radius: 25px; width: 100%; margin-top: 15px; border: none; }
</style>
""", unsafe_allow_html=True)

# --- TAROT KARTLARI ---
tarot_deck = {
    "Joker": "https://upload.wikimedia.org/wikipedia/commons/9/90/RWS_Tarot_00_Fool.jpg",
    "Büyücü": "https://upload.wikimedia.org/wikipedia/commons/d/de/RWS_Tarot_01_Magician.jpg",
    "Azize": "https://upload.wikimedia.org/wikipedia/commons/8/88/RWS_Tarot_02_High_Priestess.jpg",
    "İmparatoriçe": "https://upload.wikimedia.org/wikipedia/commons/d/d2/RWS_Tarot_03_Empress.jpg",
    "Aşıklar": "https://upload.wikimedia.org/wikipedia/commons/3/3a/RWS_Tarot_06_Lovers.jpg",
    "Savaş Arabası": "https://upload.wikimedia.org/wikipedia/commons/9/9b/RWS_Tarot_07_Chariot.jpg",
    "Güç": "https://upload.wikimedia.org/wikipedia/commons/f/f5/RWS_Tarot_08_Strength.jpg",
    "Ermiş": "https://upload.wikimedia.org/wikipedia/commons/4/4d/RWS_Tarot_09_Hermit.jpg",
    "Kader Çarkı": "https://upload.wikimedia.org/wikipedia/commons/3/3c/RWS_Tarot_10_Wheel_of_Fortune.jpg",
    "Adalet": "https://upload.wikimedia.org/wikipedia/commons/e/e0/RWS_Tarot_11_Justice.jpg",
    "Asılan Adam": "https://upload.wikimedia.org/wikipedia/commons/2/2b/RWS_Tarot_12_Hanged_Man.jpg",
    "Ölüm": "https://upload.wikimedia.org/wikipedia/commons/d/d7/RWS_Tarot_13_Death.jpg",
    "Şeytan": "https://upload.wikimedia.org/wikipedia/commons/5/55/RWS_Tarot_15_Devil.jpg",
    "Yıkılan Kule": "https://upload.wikimedia.org/wikipedia/commons/5/53/RWS_Tarot_16_Tower.jpg",
    "Yıldız": "https://upload.wikimedia.org/wikipedia/commons/d/db/RWS_Tarot_17_Star.jpg",
    "Ay": "https://upload.wikimedia.org/wikipedia/commons/7/7f/RWS_Tarot_18_Moon.jpg",
    "Güneş": "https://upload.wikimedia.org/wikipedia/commons/1/17/RWS_Tarot_19_Sun.jpg",
    "Dünya": "https://upload.wikimedia.org/wikipedia/commons/f/ff/RWS_Tarot_21_World.jpg"
}

# --- AYARLAR ---
with st.sidebar:
    st.title("⚙️ Ayarlar")
    st.audio(MUSIC_URL, format="audio/ogg")
    
    # API KEY
    api_key = None
    if 'GOOGLE_API_KEY' in st.secrets:
        api_key = st.secrets['GOOGLE_API_KEY']
        st.success("Yapay Zeka Bağlı 🟢")
    else:
        api_key = st.text_input("Google API Key", type="password")

# MODELLERİ BAŞLAT (KLASİK VERSİYON - GARANTİ ÇALIŞIR)
model_text = None  # Tarot için
model_vision = None # Kahve için

if api_key:
    try:
        genai.configure(api_key=api_key)
        # 1. Metin Modeli (Tarot)
        model_text = genai.GenerativeModel('gemini-pro') 
        # 2. Görüntü Modeli (Kahve)
        model_vision = genai.GenerativeModel('gemini-pro-vision')
    except Exception as e:
        st.error(f"Model Bağlantı Hatası
