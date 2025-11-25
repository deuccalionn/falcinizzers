import streamlit as st
import time
import random

# --- KÜTÜPHANE KONTROLÜ (HATA YAKALAYICI) ---
try:
    from PIL import Image
    import google.generativeai as genai
except ImportError as e:
    st.error(f"HATA: Kütüphane eksik! requirements.txt dosyasına 'Pillow' ve 'google-generativeai' yazdığından emin ol.\nDetay: {e}")
    st.stop()

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Mistik Falcı", page_icon="🔮", layout="wide")

# --- TASARIM (CSS) ---
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at center, #2e0249 0%, #000000 100%); color: #fff; }
    h1 { color: #FFD700 !important; font-family: 'Georgia', serif; text-shadow: 2px 2px 4px #000; text-align: center; }
    .mystic-card { background: rgba(255,255,255,0.1); border: 1px solid #FFD700; border-radius: 15px; padding: 20px; margin-top: 20px; text-align: center; color: #eee; }
    .stButton>button { background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%); color: white; border: none; padding: 12px 24px; border-radius: 25px; width: 100%; font-size: 18px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# --- SABİT LİNKLER ---
CARD_BACK = "https://i.pinimg.com/originals/70/4f/2e/704f2e04eb58172c3426e959600994f3.jpg"
MUSIC_URL = "https://upload.wikimedia.org/wikipedia/commons/0/0b/Erik_Satie_-_Gnossienne_1.ogg"

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

# --- KENAR ÇUBUĞU ---
with st.sidebar:
    st.title("⚙️ Ayarlar")
    st.caption("Mistik Müzik")
    st.audio(MUSIC_URL, format="audio/ogg")
    st.markdown("---")
    
    # API KEY
    if 'GOOGLE_API_KEY' in st.secrets:
        api_key = st.secrets['GOOGLE_API_KEY']
        st.success("Yapay Zeka Bağlı 🟢")
    else:
        api_key = st.text_input("Google API Key", type="password")

# Modeli Başlat
model = None
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except: pass

# --- ANA BAŞLIK ---
st.title("✨ MİSTİK FALCI ✨")
tab1, tab2 = st.tabs(["☕ KAHVE FALI", "🎴 TAROT FALI"])

# --- TAB 1: KAHVE FALI ---
with tab1:
    st.write("### Kahve Fincanını Yükle")
    isim = st.text_input("Adın:", key="k_isim")
    durum = st.selectbox("Niyetin:", ["Genel", "Aşk", "Kariyer", "Para"], key="k_durum")
    uploaded_file = st.file_uploader("Fincan Fotoğrafı", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_file and st.button("KAHVE FALIMA BAK"):
        if not isim:
            st.warning("Adını yazmadın...")
        else:
            image = Image.open(uploaded_file)
            st.image(image, width=300)
            with st.spinner("Yorumlanıyor..."):
                fal_metni = "API Anahtarı yok. (Demo Modu)"
                if model:
                    try:
                        prompt = f"Falcı ol. Ad: {isim}. Fincanı yorumla. Mistik, 3 paragraf."
                        res = model.generate_content([prompt, image])
                        fal_metni = res.text
                    except Exception as e: fal_metni = f"Hata: {e}"
                st.balloons()
                st.markdown(f'<div class="mystic-card"><h3>☕ Falcı Bacı:</h3><p>{fal_metni}</p></div>', unsafe_allow_html=True)

# --- TAB 2: TAROT FALI ---
with tab2:
    st.write("### 🎴 Kartlarını Seç")
    
    # Hafıza
    if 'tarot_durum' not in st.session_state:
        st.session_state['tarot_durum'] = 'kapali'
        st.session_state['secilen_kartlar'] = []
        st.session_state['tarot_yorum'] = ""

    # Sıfırlama Butonu
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
            
            # Yorum
            yorum = "Demo Modu. (API Key gerekli)"
            if model:
                try:
                    res = model.generate_content(f"Tarot bak. Kartlar: {kartlar}. Mistik hikaye yaz.")
                    yorum = res.text
                except: pass
            
            st.session_state['tarot_yorum'] = yorum
            st.session_state['tarot_durum'] = 'acik'
            st.rerun()

    else:
        k = st.session_state['secilen_kartlar']
        with c1: st.image(tarot_deck[k[0]], caption=f"GEÇMİŞ: {k[0]}")
        with c2: st.image(tarot_deck[k[1]], caption=f"ŞİMDİ: {k[1]}")
        with c3: st.image(tarot_deck[k[2]], caption=f"GELECEK: {k[2]}")
        
        st.balloons()
        st.markdown(f'<div class="mystic-card"><h3>🎴 Yorum:</h3><p>{st.session_state["tarot_yorum"]}</p></div>', unsafe_allow_html=True)
