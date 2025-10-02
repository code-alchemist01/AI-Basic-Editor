import streamlit as st
import os
from dotenv import load_dotenv
from database import DatabaseManager
from gemini_client import GeminiClient
from datetime import datetime

# Environment variables yükle
load_dotenv()

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="AI Kod Editörü",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .user-message {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }
    
    .ai-message {
        background: #f3e5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #9c27b0;
    }
    
    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    
    .status-error {
        background: #f8d7da;
        color: #721c24;
        padding: 0.5rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Session state'i başlat"""
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = None
    if 'gemini_client' not in st.session_state:
        st.session_state.gemini_client = GeminiClient()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'is_connected' not in st.session_state:
        st.session_state.is_connected = False
    if 'saved_api_key' not in st.session_state:
        st.session_state.saved_api_key = ''

def setup_database():
    """Veritabanını kur"""
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        st.session_state.db_manager = DatabaseManager(db_url)
        if st.session_state.db_manager.connect():
            st.session_state.db_manager.create_tables()
            return True
    return False

def main():
    initialize_session_state()
    
    # Ana başlık
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Kod Editörü</h1>
        <p>Uzman seviyesinde kod yazma asistanınız</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - Ayarlar
    with st.sidebar:
        st.header("⚙️ Ayarlar")
        
        # API Key girişi - kullanıcı manuel olarak girecek
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="API anahtarınızı buraya girin...",
            help="Gemini API anahtarınızı https://makersuite.google.com/app/apikey adresinden alabilirsiniz"
        )
        
        model_name = st.selectbox(
            "Model Seçin",
            ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
            index=0
        )
        
        # Bağlantı testi
        if st.button("🔗 Bağlantıyı Test Et"):
            if api_key:
                success, message = st.session_state.gemini_client.connect(api_key, model_name)
                if success:
                    st.session_state.is_connected = True
                    st.markdown(f'<div class="status-success">✅ {message}</div>', unsafe_allow_html=True)
                    
                    # Veritabanını kur
                    if setup_database():
                        st.success("📊 Veritabanı bağlantısı başarılı!")
                else:
                    st.session_state.is_connected = False
                    st.markdown(f'<div class="status-error">❌ {message}</div>', unsafe_allow_html=True)
            else:
                st.error("Lütfen API key girin!")
        
        # Bağlantı durumu
        if st.session_state.is_connected:
            st.markdown('<div class="status-success">🟢 Bağlı</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-error">🔴 Bağlı değil</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Chat geçmişini temizle
        if st.button("🗑️ Geçmişi Temizle"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Ana chat arayüzü
    if st.session_state.is_connected:
        st.header("💬 Chat Arayüzü")
        
        # Chat geçmişini göster
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>👤 Sen:</strong><br>
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="ai-message">
                        <strong>🤖 AI Kod Editörü:</strong><br>
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Mesaj girişi
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Kod yazma isteğinizi girin:",
                placeholder="Örnek: Python ile bir web scraper yaz, React ile todo app oluştur, SQL sorgu optimizasyonu yap...",
                height=100
            )
            
            col1, col2 = st.columns([1, 4])
            with col1:
                submit_button = st.form_submit_button("📤 Gönder", use_container_width=True)
        
        # Mesaj işleme
        if submit_button and user_input.strip():
            # Kullanıcı mesajını ekle
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input,
                'timestamp': datetime.now()
            })
            
            # AI yanıtı al
            with st.spinner("🤖 AI kod yazıyor..."):
                success, ai_response = st.session_state.gemini_client.generate_code_response(user_input)
                
                if success:
                    # AI yanıtını ekle
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': ai_response,
                        'timestamp': datetime.now()
                    })
                    
                    # Veritabanına kaydet
                    if st.session_state.db_manager:
                        token_count = st.session_state.gemini_client.get_token_count(user_input)
                        message_id = st.session_state.db_manager.save_message(
                            user_input, 
                            "user", 
                            int(token_count)
                        )
                        if message_id:
                            st.session_state.db_manager.save_knowledge(message_id, ai_response)
                else:
                    st.error(f"Hata: {ai_response}")
            
            st.rerun()
    
    else:
        st.warning("🔑 Lütfen önce Gemini API key'inizi girin ve bağlantıyı test edin.")
        
        # Örnek kullanım
        st.header("📋 Örnek Kullanım")
        st.markdown("""
        **Bu AI kod editörü ile neler yapabilirsiniz:**
        
        - 🐍 **Python**: Web uygulamaları, veri analizi, makine öğrenmesi
        - 🌐 **Web**: React, Vue, Angular, Node.js projeleri
        - 📱 **Mobil**: React Native, Flutter uygulamaları
        - 🗄️ **Veritabanı**: SQL sorguları, ORM kullanımı
        - 🔧 **DevOps**: Docker, CI/CD, cloud deployment
        - 🧠 **AI/ML**: TensorFlow, PyTorch, scikit-learn
        
        **Örnek promptlar:**
        - "Python Flask ile REST API yaz"
        - "React ile responsive navbar komponenti oluştur"
        - "PostgreSQL veritabanı optimizasyonu yap"
        - "Docker ile multi-stage build yaz"
        """)

if __name__ == "__main__":
    main()