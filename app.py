import streamlit as st
import time
import random
from PIL import Image

# Google Gemini Kütüphanesi
try:
    import google.generativeai as genai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Mistik Falcı", page_icon="🔮", layout="wide")

# --- TAROT KARTLARI VERİTABANI (Resimli - Major Arcana) ---
tarot_deck = {
    "Joker (The Fool)": "https://upload.wikimedia.org/wikipedia/commons/9/90/RWS_Tarot_00_Fool.jpg",
    "Büyücü (The Magician)": "https://upload.wikimedia.org/wikipedia/commons/d/de/RWS_Tarot_01_Magician.jpg",
    "Azize (High Priestess)": "https://upload.wikimedia.org/wikipedia/commons/8/88/RWS_Tarot_02_High_Priestess.jpg",
    "İmparatoriçe (The Empress)": "https://upload.wikimedia.org/wikipedia/commons/d/d2/RWS_Tarot_03_Empress.jpg",
    "İmparator (The Emperor)": "https://upload.wikimedia.org/wikipedia/commons/c/c5/RWS_Tarot_04_Emperor.jpg",
    "Aziz (The Hierophant)": "https://upload.wikimedia.org/wikipedia/commons/8/8d/RWS_Tarot_05_Hierophant.jpg",
    "Aşıklar (The Lovers)": "https://upload.wikimedia.org/wikipedia/commons/3/3a/RWS_Tarot_06_Lovers.jpg",
    "Savaş Arabası (The Chariot)": "https://upload.wikimedia.org/wikipedia/commons/9/9b/RWS_Tarot_07_Chariot.jpg",
    "Güç (Strength)": "https://upload.wikimedia.org/wikipedia/commons/f/f5/RWS_Tarot_08_Strength.jpg",
    "Ermiş (The Hermit)": "https://upload.wikimedia.org/wikipedia/commons/4/4d/RWS_Tarot_09_Hermit.jpg",
    "Kader Çarkı (Wheel of Fortune)": "https://upload.wikimedia.org/wikipedia/commons/3/3c/RWS_Tarot_10_Wheel_of_Fortune.jpg",
    "Adalet (Justice)": "https://upload.wikimedia.org/wikipedia/commons/e/e0/RWS_Tarot_11_Justice.jpg",
    "Asılan Adam (Hanged Man)": "https://upload.wikimedia.org/wikipedia/commons/2/2b/RWS_Tarot_12_Hanged_Man.jpg",
    "Ölüm (Death)": "https://upload.wikimedia.org/wikipedia/commons/d/d7/RWS_Tarot_13_Death.jpg",
    "Denge (Temperance)": "https://upload.wikimedia.org/wikipedia/commons/f/f8/RWS_Tarot_14_Temperance.jpg",
    "Şeytan (The Devil)": "https://upload.wikimedia.org/wikipedia/commons/5/55/RWS_Tarot_15_Devil.jpg",
    "Yıkılan Kule (The Tower)": "https://upload.wikimedia.org/wikipedia/commons/5/53/RWS_Tarot_16_Tower.jpg",
    "Yıldız (The Star)": "https://upload.wikimedia.org/wikipedia/commons/d/db/RWS_Tarot_17_Star.jpg",
    "Ay (The Moon)": "https://upload.wikimedia.org/wikipedia/commons/7/7f/RWS_Tarot_18_Moon.jpg",
    "Güneş (The Sun)": "https://upload.wikimedia.org/wikipedia/commons/1/17/RWS_Tarot_19_Sun.jpg",
    "Mahkeme (Judgement)": "https://upload.wikimedia.org/wikipedia/commons/d/dd/RWS_Tarot_20_Judgement.jpg",
    "Dünya (The World)": "https://upload.wikimedia.org/wikipedia/commons/f/ff/RWS_Tarot_21_World.jpg"
}

# Kart Arkası Görseli
CARD_BACK_URL = "https://i.pinimg.com/originals/70/4f/2e/704f2e04eb58172c3426e959600994f3.jpg"

# --- TASARIM (CSS) ---
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at center, #1a0b2e 0%, #000000 100%);
        color: #fff;
    }
    h1, h2, h3 {
        font-family: 'Georgia', serif;
        color: #FFD700 !important;
        text-shadow: 0px 0px 10px rgba(255, 215, 0, 0.5);
        text-align: center;
    }
    .mystic-card {
        background: rgba(25, 25, 25, 0.9);
        border: 1px solid #FFD700;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
        margin-top: 20px;
        text-align: left;
        color: #ddd;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border: none;
        border-radius: 25px;
        font-size: 18px;
        padding: 12px 24px;
        width: 100%;
        margin-top: 15px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0 5px 15px rgba(100, 100, 255, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- API AYARLARI ---
with st.sidebar:
    st.title("⚙️ Ayarlar")
    if 'GOOGLE_API_KEY' in st.secrets:
        api_key = st.secrets['GOOGLE_API_KEY']
        st.success("Sistem Anahtarı Aktif! 🟢")
    else:
        api_key = st.text_input("Google API Key", type="password")
        st.caption("Key girilmezse Demo Modu çalışır.")

model = None
if api_key and AI_AVAILABLE:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"API Hatası: {e}")

# --- ANA BAŞLIK ---
st.title("✨ MİSTİK FALCI ✨")
st.markdown("<p style='text-align:center; color:#ccc;'>Yıldızlar senin için ne söylüyor?</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["☕ KAHVE FALI", "🎴 TAROT FALI"])

# --- TAB 1: KAHVE FALI ---
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3054/3054889.png", width=120)
    with col2:
        st.write("### Fincanını Yükle")
        isim = st.text_input("Adın:", key="k_isim")
        durum = st.selectbox("Niyetin:", ["Genel", "Aşk", "Kariyer", "Para", "Sağlık"], key="k_durum")

    uploaded_file = st.file_uploader("Fincan Fotoğrafı", type=['jpg', 'png', 'jpeg'])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Fincanın", width=300)

        if st.button("FAL
