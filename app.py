import streamlit as st
import time
import random

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Mistik Falcı",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- TASARIM (CSS) ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom, #1a0b2e, #000000);
        color: #e0e0e0;
    }
    h1 {
        text-align: center;
        color: #d4af37; /* Altın Rengi */
        font-family: 'Georgia', serif;
        text-shadow: 2px 2px 4px #000000;
    }
    .stButton>button {
        background: linear-gradient(90deg, #43cea2 0%, #185a9d 100%);
        color: white;
        border: none;
        border-radius: 12px;
        height: 50px;
        width: 100%;
        font-weight: bold;
        font-size: 16px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #d4af37;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 215, 0, 0.1);
        color: white;
    }
    .info-box {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #d4af37;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- BAŞLIK ---
st.title("🔮 MİSTİK KAPILAR")
st.markdown("<p style='text-align: center; color: #aaa;'>Geçmişin sırları, geleceğin anahtarları...</p>", unsafe_allow_html=True)

# --- API KEY GİRİŞİ (Kenar Çubuğu) ---
with st.sidebar:
    st.header("⚙️ Ayarlar")
    api_key = st.text_input("Google Gemini API Key", type="password")
    st.info("API Key girilmezse Demo Modu (Simülasyon) çalışır.")

# --- SEKME SİSTEMİ ---
tab1, tab2 = st.tabs(["☕ KAHVE FALI", "🎴 TAROT FALI"])

# --- TAB 1: KAHVE FALI ---
with tab1:
    st.header("Fincanını Yorumla")
    isim = st.text_input("Adın nedir?", placeholder="Örn: Ece")
    durum = st.selectbox("İlişki Durumu", ["Seçiniz...", "Yalnız", "Platonik", "İlişkisi Var", "Evli", "Karmaşık"])
    
    uploaded_file = st.file_uploader("Fincan Fotoğrafı", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_file:
        st.image(uploaded_file, caption='Senin Fincanın', use_column_width=True)
    
    if st.button("Kahve Falıma Bak ✨"):
        if not isim or durum == "Seçiniz...":
            st.warning("Lütfen adını ve durumunu gir güzelim.")
        else:
            with st.spinner("Telveler okunuyor..."):
                time.sleep(3) # Mistik bekleme
                
                # DEMO MODU CEVABI (Şimdilik)
                fal_sonucu = f"""
                **Sevgili {isim}, fincanın çok şey anlatıyor...**
                
                Yüreğin biraz sıkışmış ama ferahlık kapıda. Fincanın tam ortasında kocaman bir 'Yol' var. 
                Bu yol temiz ve aydınlık. Yakın zamanda beklediğin bir haber tez vakitte sana ulaşacak.
                
                {durum} durumunla ilgili olarak; birisi senin hakkında konuşuyor ama iyi anlamda. 
                Kısa boylu, esmer birinden bir destek görebilirsin.
                """
                
                st.markdown(f'<div class="info-box">{fal_sonucu}</div>', unsafe_allow_html=True)

# --- TAB 2: TAROT FALI ---
with tab2:
    st.header("Kartlarını Seç")
    st.write("Senin için 3 kartlık 'Geçmiş, Şimdi, Gelecek' açılımı yapacağım.")
    
    tarot_isim = st.text_input("Niyetin (İsteğe bağlı)", placeholder="Örn: Kariyerim ne olacak?")
    
    if st.button("Kartları Çek ve Yorumla 🃏"):
        with st.spinner("Kartlar karıştırılıyor... Enerjin aktarılıyor..."):
            time.sleep(3)
            
            # Tarot Kartları Listesi (Demo için)
            kartlar = ["Kupa Kraliçesi", "Joker", "Kılıç Üçlüsü", "Aşıklar", "Yıkılan Kule", "Güneş", "Ay", "İmparatoriçe", "Asılan Adam", "Dünya"]
            secilenler = random.sample(kartlar, 3)
            
            # DEMO YORUMU
            tarot_sonucu = f"""
            🎴 **GEÇMİŞ: {secilenler[0]}**
            Geçmişte yaşadığın bir olay seni derinden etkilemiş, ama seni güçlendirmiş.
            
            🎴 **ŞİMDİ: {secilenler[1]}**
            Şu an tam bir karar aşamasındasın. Enerjin çok yüksek ama nereye harcayacağını bilemiyorsun.
            
            🎴 **GELECEK: {secilenler[2]}**
            Gelecekte seni büyük bir aydınlanma bekliyor. Sabırlı olursan mükafatını alacaksın.
            """
            
            st.markdown(f'<div class="info-box">{tarot_sonucu}</div>', unsafe_allow_html=True)
            st.balloons()
