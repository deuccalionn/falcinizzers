import streamlit as st
import time
import random
from PIL import Image

# --- KÜTÜPHANE KONTROLÜ ---
try:
    import google.generativeai as genai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Mistik Falcı", page_icon="🔮", layout="wide")

# --- TAROT VERİTABANI ---
tarot_deck = {
    "Joker": "https://upload.wikimedia.org/wikipedia/commons/9/90/RWS_Tarot_00_Fool.jpg",
    "Büyücü": "https://upload.wikimedia.org/wikipedia/commons/d/de/RWS_Tarot_01_Magician.jpg",
    "Azize": "https://upload.wikimedia.org/wikipedia/commons/8/88/RWS_Tarot_02_High_Priestess.jpg",
    "İmparatoriçe": "https://upload.wikimedia.org/wikipedia/commons/d/d2/RWS_Tarot_03_Empress.jpg",
    "İmparator": "https://upload.wikimedia.org/wikipedia/commons/c/c5/RWS_Tarot_04_Emperor.jpg",
    "Aziz": "https://upload.wikimedia.org/wikipedia/commons/8/8d/RWS_Tarot_05_Hierophant.jpg",
    "Aşıklar": "https://upload.wikimedia.org/wikipedia/commons/3/3a/RWS_Tarot_06_Lovers.jpg",
    "Savaş Arabası": "https://upload.wikimedia.org/wikipedia/commons/9/9b/RWS_Tarot_07_Chariot.jpg",
    "Güç": "https://upload.wikimedia.org/wikipedia/commons/f/f5/RWS_Tarot_08_Strength.jpg",
    "Ermiş": "https://upload.wikimedia.org/wikipedia/commons/4/4d/RWS_Tarot_09_Hermit.jpg",
    "Kader Çarkı": "https://upload.wikimedia.org/wikipedia/commons/3/3c/RWS_Tarot_10_Wheel_of_Fortune.jpg",
    "Adalet": "https://upload.wikimedia.org/wikipedia/commons/e/e0/RWS_Tarot_11_Justice.jpg",
    "Asılan Adam": "https://upload.wikimedia.org/wikipedia/commons/2/2b/RWS_Tarot_12_Hanged_Man.jpg",
    "Ölüm": "https://upload.wikimedia.org/wikipedia/commons/d/d7/RWS_Tarot_13_Death.jpg",
    "Denge": "https://upload.wikimedia.org/wikipedia/commons/f/f8/RWS_Tarot_14_Temperance.jpg",
    "Şeytan": "https://upload.wikimedia.org/wikipedia/commons/5/55/RWS_Tarot_15_Devil.jpg",
    "Yıkılan Kule": "https://upload.wikimedia.org/wikipedia/commons/5/53/RWS_Tarot_16_Tower.jpg",
    "Yıldız": "https://upload.wikimedia.org/wikipedia/commons/d/db/RWS_Tarot_17_Star.jpg",
    "Ay": "https://upload.wikimedia.org/wikipedia/commons/7/7f/RWS_Tarot_18_Moon.jpg",
    "Güneş": "https://upload.wikimedia.org/wikipedia/commons/1/17/RWS_Tarot_19_Sun.jpg",
    "Mahkeme": "https://upload.wikimedia.org/wikipedia/commons/d/dd/RWS_Tarot_20_Judgement.jpg",
    "Dünya": "https://upload.wikimedia.org/wikipedia/commons/f/ff/RWS_Tarot_21_World.jpg"
}
CARD_BACK_URL = "https://i.pinimg.com/originals/70/4f/2e/704f2e04eb58172c3426e959600994f3.jpg"

# --- TASARIM ---
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at center, #1a0b2e 0%, #000000 100%); color: #fff; }
    h1, h2, h3 { font-family: 'Georgia', serif; color: #FFD700 !important; text-shadow: 0px 0px 10px rgba(255, 215, 0, 0.5); text-align: center; }
    .mystic-card { background: rgba(25, 25, 25, 0.9); border: 1px solid #FFD700; border-radius: 15px; padding: 20px; box-shadow: 0 0 20px rgba(255, 215, 0, 0.3); margin-top: 20px; color: #ddd; }
    .stButton>button { background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%); color: white; border: none; border-radius: 25px; font-size: 18px; padding: 12px 24px; width: 100%; margin-top: 15px; }
</style>
""", unsafe_allow_html=True)

# --- API KEY ---
with st.sidebar:
    st.title("⚙️ Ayarlar")
    if 'GOOGLE_API_KEY' in st.secrets:
        api_key = st.secrets['GOOGLE_API_KEY']
        st.success("Sistem Anahtarı Aktif! 🟢")
    else:
        api_key = st.text_input("Google API Key", type="password")

model = None
if api_key and AI_AVAILABLE:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except: pass

# --- ANA EKRAN ---
st.title("✨ MİSTİK FALCI ✨")
tab1, tab2 = st.tabs(["☕ KAHVE FALI", "🎴 TAROT FALI"])

# --- TAB 1: KAHVE FALI ---
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1: st.image("https://cdn-icons-png.flaticon.com/512/3054/3054889.png", width=100)
    with col2:
        isim = st.text_input("Adın:", key="k_isim")
        durum = st.selectbox("Niyetin:", ["Genel", "Aşk", "Kariyer", "Para"], key="k_durum")
    uploaded_file = st.file_uploader("Fincan Fotoğrafı", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_file and st.button("KAHVE FALIMA BAK"):
        image = Image.open(uploaded_file)
        st.image(image, width=300)
        with st.spinner("Fincan okunuyor..."):
            fal_metni = "API Anahtarı yok. (Demo Modu)"
            if model:
                try:
                    res = model.generate_content([f"Falcı ol. Ad: {isim}. Fincanı yorumla.", image])
                    fal_metni = res.text
                except Exception as e: fal_metni = f"Hata: {e}"
            st.markdown(f'<div class="mystic-card">{fal_metni}</div>', unsafe_allow_html=True)

# --- TAB 2: TAROT FALI (HAFIZALI VERSİYON) ---
with tab2:
    st.write("### 🎴 Kartlarını Seç")
    
    # HAFIZA (SESSION STATE) BAŞLATMA - BURASI ÇOK ÖNEMLİ
    if 'tarot_durum' not in st.session_state:
        st.session_state['tarot_durum'] = 'kapali'
    if 'secilen_kartlar' not in st.session_state:
        st.session_state['secilen_kartlar'] = [] # Kart isimlerini tutar
    if 'tarot_yorum' not in st.session_state:
        st.session_state['tarot_yorum'] = ""

    # YENİ FAL BAK BUTONU (Sıfırlamak için)
    if st.session_state['tarot_durum'] == 'acik':
        if st.button("🔄 Yeni Tarot Açılımı Yap"):
            st.session_state['tarot_durum'] = 'kapali'
            st.session_state['secilen_kartlar'] = []
            st.session_state['tarot_yorum'] = ""
            st.rerun()

    # GÖRÜNTÜLEME ALANI
    col_t1, col_t2, col_t3 = st.columns(3)

    # DURUM 1: HENÜZ BUTONA BASILMADI (KAPALI KARTLAR)
    if st.session_state['tarot_durum'] == 'kapali':
        with col_t1: st.image(CARD_BACK_URL, caption="Geçmiş")
        with col_t2: st.image(CARD_BACK_URL, caption="Şimdi")
        with col_t3: st.image(CARD_BACK_URL, caption="Gelecek")
        
        # BUTONA BASILINCA NE OLACAK?
        if st.button("KARTLARI ÇEK VE YORUMLA 🔮", key="btn_tarot_cek"):
            # 1. Kartları Seç ve Hafızaya At
            kart_isimleri = random.sample(list(tarot_deck.keys()), 3)
            st.session_state['secilen_kartlar'] = kart_isimleri
            
            # 2. Animasyonlu Gösterim (Sadece o anlık)
            with col_t1:
                with st.spinner("Geçmiş..."): time.sleep(0.5)
                st.image(tarot_deck[kart_isimleri[0]])
            with col_t2:
                with st.spinner("Şimdi..."): time.sleep(0.5)
                st.image(tarot_deck[kart_isimleri[1]])
            with col_t3:
                with st.spinner("Gelecek..."): time.sleep(0.5)
                st.image(tarot_deck[kart_isimleri[2]])
            
            # 3. Yorumu Hazırla ve Hafızaya At
            yorum = ""
            if model:
                try:
                    prompt = f"Tarot bak. Kartlar: {kart_isimleri}. Mistik bir hikaye anlat."
                    res = model.generate_content(prompt)
                    yorum = res.text
                except: yorum = "Bağlantı hatası."
            else:
                yorum = f"Kartların: {kart_isimleri}. (Demo Modu)"
            
            st.session_state['tarot_yorum'] = yorum
            st.session_state['tarot_durum'] = 'acik'
            st.rerun() # Sayfayı yenile ki hafızadan okusun

    # DURUM 2: FALA BAKILDI (AÇIK KARTLAR VE YORUM)
    elif st.session_state['tarot_durum'] == 'acik':
        # Hafızadaki kartları göster (Animasyonsuz, direkt gelir)
        kartlar = st.session_state['secilen_kartlar']
        with col_t1: st.image(tarot_deck[kartlar[0]], caption=f"GEÇMİŞ: {kartlar[0]}")
        with col_t2: st.image(tarot_deck[kartlar[1]], caption=f"ŞİMDİ: {kartlar[1]}")
        with col_t3: st.image(tarot_deck[kartlar[2]], caption=f"GELECEK: {kartlar[2]}")
        
        st.balloons()
        st.markdown(f"""
        <div class="mystic-card">
            <h3>🎴 Kartların Mesajı:</h3>
            <p>{st.session_state['tarot_yorum']}</p>
        </div>
        """, unsafe_allow_html=True)
