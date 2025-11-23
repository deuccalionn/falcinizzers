import streamlit as st
import time
import os
from openai import OpenAI

# --- SAYFA AYARLARI (MOBİL UYUMLU) ---
st.set_page_config(
    page_title="Mistik Fal",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ÖZEL TASARIM (CSS MAKYAJI) ---
# Bu kısım uygulamanın "beyaz dosya" gibi görünmesini engeller,
# arka planı ve butonları özelleştirir.
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom, #2c003e, #000000);
        color: #ffffff;
    }
    h1 {
        text-align: center;
        color: #FFD700 !important;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 2px 2px 4px #000000;
    }
    .stButton>button {
        color: white;
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
        border: none;
        border-radius: 20px;
        height: 50px;
        width: 100%;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 8px 20px rgba(0,0,0,0.5);
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 10px;
        border: 1px solid #6a11cb;
    }
    p {
        font-size: 16px;
    }
    .info-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #FFD700;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- BAŞLIK VE GİRİŞ ---
st.title("🔮 MİSTİK FALCI")
st.markdown("<p style='text-align: center; color: #ddd;'>Yıldızların ve kahvenin sana bir mesajı var...</p>", unsafe_allow_html=True)

# --- KENAR ÇUBUĞU (GİZLİ AYARLAR) ---
with st.sidebar:
    st.header("⚙️ Yönetici Paneli")
    api_key = st.text_input("OpenAI API Key", type="password", help="Gerçek fal yorumu için gereklidir.")
    st.markdown("---")
    st.info("API anahtarı girmezsen demo modunda çalışır.")

# --- KULLANICI GİRİŞİ ---
col1, col2 = st.columns(2)
with col1:
    isim = st.text_input("İsmin", placeholder="Adın ne?")
with col2:
    burc = st.selectbox("Burcun", ["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"])

durum = st.radio("İlişki Durumu", ["Yalnızım", "Karmaşık", "Mutlu İlişki", "Platonik"], horizontal=True)

uploaded_file = st.file_uploader("Fincanının Fotoğrafını Yükle", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    st.image(uploaded_file, caption='Fincanın Okunuyor...', use_column_width=True)

# --- FAL BAKMA BUTONU ---
if st.button("FALIMA BAK ✨"):
    if not isim:
        st.warning("Lütfen önce ismini bahşet güzelim.")
    else:
        # Yükleme Animasyonu
        progress_text = "Enerjiler yoğunlaşıyor..."
        my_bar = st.progress(0, text=progress_text)
        
        for percent_complete in range(100):
            time.sleep(0.02)
            my_bar.progress(percent_complete + 1, text="Yıldızlar hizalanıyor...")
        
        time.sleep(0.5)
        my_bar.empty()

        st.markdown("---")
        
        # --- YAPAY ZEKA MANTIĞI ---
        fal_yorumu = ""
        
        if api_key:
            try:
                client = OpenAI(api_key=api_key)
                # Burada gerçek Vision API çağrısı yapılır.
                # Basitlik için şimdilik metin tabanlı simülasyon yapıyoruz.
                prompt = f"Sen mistik bir falcısın. Kullanıcı adı: {isim}, Burcu: {burc}, Durumu: {durum}. Ona çok etkileyici, sanki fincanını görüyormuşsun gibi detaylı, mistik ve hafif esprili bir kahve falı yaz. Emojiler kullan."
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                fal_yorumu = response.choices[0].message.content
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
                fal_yorumu = "Evrenle bağlantı kurulamadı. Lütfen API anahtarını kontrol et."
        else:
            # DEMO MODU (Arkadaşlarına göstermek için API key yoksa bu çalışır)
            fal_yorumu = f"""
            🌑 **Ey {isim}, fincanın bana sırlar fısıldıyor...**
            
            Öncelikle fincanın dibinde büyük bir sıkıntı görüyorum ama merak etme, bu sıkıntı "haneye ay doğması" gibi aydınlığa çıkacak. {burc} burcunun inadı biraz üzerinde ama kalbin temiz.
            
            Üç vakte kadar eline bir para veya beklediğin bir haber geçecek. 'A' harfli birinden gelecek bu haber. {durum} durumuna gelince; kartlar ve telveler bir değişimin kapıda olduğunu söylüyor.
            
            *Bir yolun var, temiz ve açık...*
            """
        
        # Sonucu süslü bir kutuda göster
        st.markdown(f"""
        <div class="info-box">
            <h3>🔮 Falcı Bacı'nın Yorumu:</h3>
            <p>{fal_yorumu}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.balloons() # Ekranda balonlar uçar (Kutlama efekti)
