import streamlit as st
import time
import random

# --- KÜTÜPHANE KONTROLÜ ---
try:
    from PIL import Image
    import google.generativeai as genai
except ImportError:
    st.error("HATA: Kütüphaneler eksik. requirements.txt dosyasını kontrol et.")
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
    st.title("Ayarlar")
    st.audio(MUSIC_URL, format="audio/ogg")
    
    api_key = None
    if 'GOOGLE_API_KEY' in st.secrets:
        api_key = st.secrets['GOOGLE_API_KEY']
        st.success("Yapay Zeka Bağlı 🟢")
    else:
        api_key = st.text_input("Google API Key", type="password")

# --- MODEL BAŞLATMA ---
model_text = None
model_vision = None

if api_key:
    try:
        genai.configure(api_key=api_key)
        # 404 hatası almamak için klasik modelleri kullanıyoruz
        model_text = genai.GenerativeModel('gemini-pro')
        model_vision = genai.GenerativeModel('gemini-pro-vision')
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")

# --- ANA EKRAN ---
st.title("✨ MİSTİK FALCI ✨")
tab1, tab2 = st.tabs(["☕ KAHVE FALI", "🎴 TAROT FALI"])

# --- KAHVE ---
with tab1:
    st.write("### Fincanını Yükle")
    isim = st.text_input("Adın:", key="k_isim")
    durum = st.selectbox("Niyetin:", ["Genel", "Aşk", "Kariyer", "Para"], key="k_durum")
    uploaded_file = st.file_uploader("Fincan Fotoğrafı", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_file and st.button("KAHVE FALIMA BAK"):
        if not model_vision:
            st.error("Model yüklenemedi. API Key kontrol et.")
        else:
            image = Image.open(uploaded_file)
            st.image(image, width=300)
            with st.spinner("Yorumlanıyor..."):
                try:
                    prompt = f"Falcı ol. Ad: {isim}. Fincanı yorumla. Mistik ol."
                    res = model_vision.generate_content([prompt, image])
                    st.markdown(f'<div class="mystic-card">{res.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Hata: {e}")

# --- TAROT ---
with tab2:
    st.write("### 🎴 Kartlarını Seç")
    if 'tarot_durum' not in st.session_state:
        st.session_state.update({'tarot_durum': 'kapali', 'secilen_kartlar': [], 'tarot_yorum': ''})

    if st.session_state['tarot_durum'] == 'acik':
        if st.button("🔄 Yeni Fal"):
            st.session_state['tarot_durum'] = 'kapali'
            st.rerun()

    c1, c2, c3 = st.columns(3)

    if st.session_state['tarot_durum'] == 'kapali':
        with c1: st.image(CARD_BACK, caption="Geçmiş")
        with c2: st.image(CARD_BACK, caption="Şimdi")
        with c3: st.image(CARD_BACK, caption="Gelecek")
        
        if st.button("KARTLARI ÇEK 🔮"):
            if not model_text:
                st.error("Model yüklenemedi. API Key kontrol et.")
            else:
                kartlar = random.sample(list(tarot_deck.keys()), 3)
                st.session_state['secilen_kartlar'] = kartlar
                
                # Animasyon
                with c1:
                    with st.spinner("."): time.sleep(0.5)
                    st.image(tarot_deck[kartlar[0]])
                with c2:
                    with st.spinner("."): time.sleep(0.5)
                    st.image(tarot_deck[kartlar[1]])
                with c3:
                    with st.spinner("."): time.sleep(0.5)
                    st.image(tarot_deck[kartlar[2]])
                
                try:
                    res = model_text.generate_content(f"Tarot bak. Kartlar: {kartlar}. Mistik hikaye yaz.")
                    st.session_state['tarot_yorum'] = res.text
                    st.session_state['tarot_durum'] = 'acik'
                    st.rerun()
                except Exception as e:
                    st.error(f"Hata: {e}")

    else:
        k = st.session_state['secilen_kartlar']
        with c1: st.image(tarot_deck[k[0]], caption=f"GEÇMİŞ: {k[0]}")
        with c2: st.image(tarot_deck[k[1]], caption=f"ŞİMDİ: {k[1]}")
        with c3: st.image(tarot_deck[k[2]], caption=f"GELECEK: {k[2]}")
        st.balloons()
        st.markdown(f'<div class="mystic-card"><h3>🎴 Yorum:</h3><p>{st.session_state["tarot_yorum"]}</p></div>', unsafe_allow_html=True)
