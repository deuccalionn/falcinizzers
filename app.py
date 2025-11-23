import streamlit as st
import time
import random

# --- SAYFA VE TASARIM AYARLARI ---
st.set_page_config(page_title="Mistik Falcı", page_icon="🔮", layout="wide")

# --- CSS İLE PROFESYONEL MAKYAJ ---
st.markdown("""
<style>
    /* Genel Arka Plan */
    .stApp {
        background: radial-gradient(circle at center, #2e0249 0%, #000000 100%);
        color: #fff;
    }
    
    /* Başlıklar */
    h1, h2, h3 {
        font-family: 'Cinzel', serif; /* Mistik font */
        color: #FFD700 !important; /* Altın sarısı */
        text-shadow: 0px 0px 10px rgba(255, 215, 0, 0.5);
        text-align: center;
    }

    /* Kart Kutuları (Tarot ve Fal Sonuçları) */
    .mystic-card {
        background: rgba(20, 20, 20, 0.8);
        border: 1px solid #FFD700;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
        margin-bottom: 20px;
        text-align: center;
        animation: fadeIn 2s;
    }

    /* Animasyon Efekti */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* Butonlar */
    .stButton>button {
        background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(106, 17, 203, 0.6);
    }

    /* Kahve Falından Sonraki Yönlendirme Kutusu */
    .upsell-box {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px dashed #fff;
        margin-top: 20px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# --- TAROT KARTLARI VERİTABANI (Resimli) ---
tarot_deck = {
    "Joker": {"img": "https://upload.wikimedia.org/wikipedia/commons/9/90/RWS_Tarot_00_Fool.jpg", "desc": "Yeni başlangıçlar, masumiyet, macera."},
    "Büyücü": {"img": "https://upload.wikimedia.org/wikipedia/commons/d/de/RWS_Tarot_01_Magician.jpg", "desc": "Yetenek, irade gücü, arzu."},
    "Azize": {"img": "https://upload.wikimedia.org/wikipedia/commons/8/88/RWS_Tarot_02_High_Priestess.jpg", "desc": "Sezgi, gizem, bilinçaltı."},
    "İmparatoriçe": {"img": "https://upload.wikimedia.org/wikipedia/commons/d/d2/RWS_Tarot_03_Empress.jpg", "desc": "Bereket, doğa, annelik."},
    "Aşıklar": {"img": "https://upload.wikimedia.org/wikipedia/commons/3/3a/RWS_Tarot_06_Lovers.jpg", "desc": "Aşk, uyum, ilişkiler, seçimler."},
    "Güç": {"img": "https://upload.wikimedia.org/wikipedia/commons/f/f5/RWS_Tarot_08_Strength.jpg", "desc": "Cesaret, şefkat, sabır."},
    "Ermiş": {"img": "https://upload.wikimedia.org/wikipedia/commons/4/4d/RWS_Tarot_09_Hermit.jpg", "desc": "İçsel rehberlik, yalnızlık, arayış."},
    "Kader Çarkı": {"img": "https://upload.wikimedia.org/wikipedia/commons/3/3c/RWS_Tarot_10_Wheel_of_Fortune.jpg", "desc": "Karmik değişim, şans, dönüm noktaları."},
    "Ölüm": {"img": "https://upload.wikimedia.org/wikipedia/commons/d/d7/RWS_Tarot_13_Death.jpg", "desc": "Bitişler, değişim, dönüşüm (Korkma, yenilenme demek)."},
    "Şeytan": {"img": "https://upload.wikimedia.org/wikipedia/commons/5/55/RWS_Tarot_15_Devil.jpg", "desc": "Bağımlılık, maddiyat, tutku."},
    "Yıkılan Kule": {"img": "https://upload.wikimedia.org/wikipedia/commons/5/53/RWS_Tarot_16_Tower.jpg", "desc": "Ani değişim, kaos, uyanış."},
    "Yıldız": {"img": "https://upload.wikimedia.org/wikipedia/commons/d/db/RWS_Tarot_17_Star.jpg", "desc": "Umut, ilham, maneviyat."},
    "Ay": {"img": "https://upload.wikimedia.org/wikipedia/commons/7/7f/RWS_Tarot_18_Moon.jpg", "desc": "Yanılsama, korku, rüyalar."},
    "Güneş": {"img": "https://upload.wikimedia.org/wikipedia/commons/1/17/RWS_Tarot_19_Sun.jpg", "desc": "Pozitiflik, başarı, canlılık."},
}

# --- YAN MENÜ ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4743/4743167.png", width=100)
    st.title("Ayarlar")
    api_key = st.text_input("API Key (Opsiyonel)", type="password")
    st.info("Key yoksa mistik demo modu çalışır.")
    
# --- ANA BAŞLIK ---
st.title("✨ MİSTİK FALCI ✨")
st.markdown("Geçmişin tozlu sayfalarından, geleceğin parlak ışıklarına...")

# --- SEKME SİSTEMİ ---
tab1, tab2 = st.tabs(["☕ KAHVE FALI", "🎴 TAROT FALI"])

# --------------------------
# TAB 1: KAHVE FALI
# --------------------------
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3054/3054889.png", width=150)
    with col2:
        st.write("### Fincanını Gönder, Kaderini Okuyalım")
        isim = st.text_input("Adın:", key="kahve_isim")
        durum = st.selectbox("Durumun:", ["Merakta", "Aşık", "Kırgın", "Umutlu", "Endişeli"], key="kahve_durum")
    
    uploaded_file = st.file_uploader("Fincan Fotoğrafı", type=['jpg', 'png'])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Senin Fincanın", width=300)
        
    if st.button("FALIMA BAK", key="kahve_btn"):
        if not isim:
            st.warning("Adını fısıldaman gerek...")
        else:
            progress_text = "Fincan dönüyor..."
            my_bar = st.progress(0, text=progress_text)
            for percent in range(100):
                time.sleep(0.02)
                my_bar.progress(percent + 1, text="Telveler şekilleniyor...")
            time.sleep(0.5)
            my_bar.empty()
            
            # FAL SONUCU
            fal_metni = f"""
            **Ey {isim}!** Fincanın bana çok şey anlatıyor...
            
            Karanlık bir sıkıntın var ama fincanın dibi ferah, yani sonu aydınlık.
            Harf görüyorum... 'M' veya 'E' harfi var isminde. Bu kişi seninle ilgili bir haber getirecek.
            Maddi konularda bir kapı aralanıyor, anahtar görüyorum.
            
            *Ama dikkat et, enerjin biraz karışık... Bunu Tarot ile netleştirmemiz lazım.*
            """
            
            st.markdown(f"""
            <div class="mystic-card">
                <h3>☕ Falcı Bacı Diyor ki:</h3>
                <p style="font-size:18px;">{fal_metni}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # TAROT'A YÖNLENDİRME (UPSELL)
            st.markdown("""
