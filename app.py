import streamlit as st
import time
import random
import os
from PIL import Image

# Google Gemini Kütüphanesi (Eğer yüklü değilse hata vermesin diye try-except)
try:
    import google.generativeai as genai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Mistik Falcı", page_icon="🔮", layout="wide")

# --- TASARIM (CSS) ---
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at center, #2e0249 0%, #000000 100%);
        color: #fff;
    }
    h1, h2, h3 {
        font-family: 'Georgia', serif;
        color: #FFD700 !important;
        text-shadow: 0px 0px 10px rgba(255, 215, 0, 0.5);
        text-align: center;
    }
    .mystic-card {
        background: rgba(20, 20, 20, 0.85);
        border: 1px solid #FFD700;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
        margin-bottom: 20px;
        text-align: center;
        color: #fff;
    }
    .stButton>button {
        background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border: none;
        border-radius: 25px;
        font-size: 18px;
        padding: 12px 24px;
        width: 100%;
        margin-top: 10px;
    }
    .stButton>button:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# --- AYARLAR VE API KEY ---
with st.sidebar:
    st.title("⚙️ Ayarlar")
    
    # 1. Önce GitHub Secrets'tan key'i almaya çalış
    if 'GOOGLE_API_KEY' in st.secrets:
        api_key = st.secrets['GOOGLE_API_KEY']
        st.success("Sistem Anahtarı Aktif! 🟢")
    else:
        # 2. Yoksa kullanıcıdan iste
        api_key = st.text_input("Google API Key", type="password")
        st.caption("Key girilmezse Demo Modu çalışır.")

# Modeli Başlat
model = None
if api_key and AI_AVAILABLE:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"API Hatası: {e}")

# --- ANA EKRAN ---
st.title("✨ MİSTİK FALCI ✨")
st.markdown("<p style='text-align:center;'>Geçmişin sırları, geleceğin anahtarları...</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["☕ KAHVE FALI", "🎴 TAROT FALI"])

# --- BÖLÜM 1: KAHVE FALI ---
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3054/3054889.png", width=150)
    with col2:
        st.write("### Fincanını Gönder")
        isim = st.text_input("Adın:", key="k_isim")
        durum = st.selectbox("Niyetin:", ["Genel", "Aşk", "Kariyer", "Para"], key="k_durum")

    uploaded_file = st.file_uploader("Fincan Fotoğrafı Yükle", type=['jpg', 'png', 'jpeg'])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Fincanın", width=300)

        if st.button("FALIMA BAK", key="btn_kahve"):
            if not isim:
                st.warning("Adını yazmadın kuzum!")
            else:
                with st.spinner("Telveler okunuyor..."):
                    fal_metni = ""
                    if model:
                        try:
                            # GERÇEK YAPAY ZEKA
                            prompt = f"Sen mistik bir falcısın. Adı {isim}, niyeti {durum}. Bu kahve fincanı fotosuna bak. Gördüğün sembolleri yorumla. 3 paragraf, mistik ve umut verici yaz."
                            response = model.generate_content([prompt, image])
                            fal_metni = response.text
                        except Exception as e:
                            fal_metni = f"Bir hata oluştu: {e}"
                    else:
                        # DEMO MODU (API YOKSA)
                        time.sleep(2)
                        fal_metni = f"**Sevgili {isim},** fincanında uzun bir yol ve aydınlık bir gelecek görüyorum. {durum} konusunda kalbini ferah tut. Yakında 'A' harfli birinden haberin var. (Bu bir demo yorumdur, gerçek yorum için API Key gereklidir.)"
                    
                    st.balloons()
                    st.markdown(f"""
                    <div class="mystic-card">
                        <h3>☕ Falcı Bacı'nın Yorumu:</h3>
                        <p>{fal_metni}</p>
                    </div>
                    """, unsafe_allow_html=True)

# --- BÖLÜM 2: TAROT FALI ---
with tab2:
    st.write("### 🎴 Kartlarını Seç")
    if st.button("KARTLARI ÇEK VE YORUMLA", key="btn_tarot"):
        kartlar = ["Joker", "Büyücü", "Azize", "İmparatoriçe", "İmparator", "Aşıklar", "Savaş Arabası", "Güç", "Ermiş", "Kader Çarkı", "Adalet", "Asılan Adam", "Ölüm", "Denge", "Şeytan", "Yıkılan Kule", "Yıldız", "Ay", "Güneş", "Mahkeme", "Dünya"]
        secilenler = random.sample(kartlar, 3)
        
        c1, c2, c3 = st.columns(3)
        c1.success(f"GEÇMİŞ: {secilenler[0]}")
        c2.warning(f"ŞİMDİ: {secilenler[1]}")
        c3.info(f"GELECEK: {secilenler[2]}")
        
        with st.spinner("Kartlar yorumlanıyor..."):
            tarot_metni = ""
            if model:
                # GERÇEK AI
                prompt_tarot = f"Tarot falı bak. Seçilenler: Geçmiş={secilenler[0]}, Şimdi={secilenler[1]}, Gelecek={secilenler[2]}. Bu kombinasyonu yorumla."
                try:
                    response_tarot = model.generate_content(prompt_tarot)
                    tarot_metni = response_tarot.text
                except:
                    tarot_metni = "Bağlantı hatası."
            else:
                # DEMO
                time.sleep(2)
                tarot_metni = f"Kartların çok güçlü çıktı! {secilenler[1]} kartı şu an bir dönüm noktasında olduğunu gösteriyor. Geleceğindeki {secilenler[2]} ise büyük bir zaferi müjdeliyor."
            
            st.markdown(f"""
            <div class="mystic-card">
                <h3>🎴 Kartların Mesajı:</h3>
                <p>{tarot_metni}</p>
            </div>
            """, unsafe_allow_html=True)
