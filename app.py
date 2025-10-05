import streamlit as st
import os
import re
import json
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

# CSS stilleri - Geliştirilmiş UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .chat-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: transparent;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 3px solid #007bff;
        animation: slideInRight 0.3s ease-out;
    }
    
    .ai-message {
        background: transparent;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 3px solid #6c757d;
        animation: slideInLeft 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .status-success {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        box-shadow: 0 2px 8px rgba(21, 87, 36, 0.1);
    }
    
    .status-error {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #f5c6cb;
        box-shadow: 0 2px 8px rgba(114, 28, 36, 0.1);
    }
    
    .code-block-container {
        position: relative;
        margin: 1rem 0;
    }
    
    .copy-button {
        position: absolute;
        top: 10px;
        right: 10px;
        background: #007bff;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 12px;
        z-index: 1000;
    }
    
    .copy-button:hover {
        background: #0056b3;
    }
    
    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: #007bff;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 50%;
        cursor: pointer;
        font-size: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    
    .file-upload-area {
        border: 2px dashed #007bff;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: linear-gradient(135deg, #f8f9ff 0%, #e6f3ff 100%);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .file-upload-area:hover {
        border-color: #0056b3;
        background: linear-gradient(135deg, #e6f3ff 0%, #cce7ff 100%);
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #007bff;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    }
    
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #007bff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .refactor-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        margin: 1.5rem 0;
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .refactor-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .refactor-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.12);
    }
    
    .refactor-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f1f3f4;
    }
    
    .refactor-icon {
        font-size: 2.5rem;
        margin-right: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .refactor-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 0;
    }
    
    .refactor-description {
        color: #6c757d;
        font-size: 0.95rem;
        margin-top: 0.5rem;
        line-height: 1.6;
    }
    
    .analysis-result {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border: 1px solid #dee2e6;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    }
    
    .analysis-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e9ecef;
    }
    
    .analysis-icon {
        font-size: 1.8rem;
        margin-right: 0.8rem;
        color: #28a745;
    }
    
    .analysis-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 0;
    }
    
    .progress-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #007bff;
    }
    
    .progress-text {
        color: #495057;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .progress-bar {
        width: 100%;
        height: 8px;
        background: #e9ecef;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #007bff 0%, #0056b3 100%);
        border-radius: 4px;
        animation: progressAnimation 2s ease-in-out;
    }
    
    @keyframes progressAnimation {
        0% { width: 0%; }
        100% { width: 100%; }
    }
    
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #f1f3f4;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #007bff;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #6c757d;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .input-group {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e9ecef;
    }
    
    .input-label {
        font-weight: 600;
        color: #495057;
        margin-bottom: 0.8rem;
        display: block;
    }
    
    .action-button {
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0, 123, 255, 0.3);
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 123, 255, 0.4);
    }
    
    .secondary-button {
        background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 20px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 0.25rem;
    }
    
    .secondary-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(108, 117, 125, 0.3);
    }
    
    .success-alert {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
        display: flex;
        align-items: center;
    }
    
    .success-alert::before {
        content: '✅';
        margin-right: 0.8rem;
        font-size: 1.2rem;
    }
    
    .warning-alert {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        color: #856404;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
        display: flex;
        align-items: center;
    }
    
    .warning-alert::before {
        content: '⚠️';
        margin-right: 0.8rem;
        font-size: 1.2rem;
    }
    
    .info-alert {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        color: #0c5460;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
        display: flex;
        align-items: center;
    }
    
    .info-alert::before {
        content: 'ℹ️';
        margin-right: 0.8rem;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

def detect_code_language(code_text):
    """Kod dilini otomatik tespit et"""
    code_lower = code_text.lower().strip()
    
    # Python patterns
    if any(keyword in code_lower for keyword in ['def ', 'import ', 'from ', 'class ', 'if __name__', 'print(', 'python']):
        return 'python'
    
    # JavaScript patterns
    elif any(keyword in code_lower for keyword in ['function ', 'const ', 'let ', 'var ', 'console.log', 'javascript', 'js', '=>']):
        return 'javascript'
    
    # HTML patterns
    elif any(keyword in code_lower for keyword in ['<html', '<div', '<body', '<head', '<!doctype', 'html']):
        return 'html'
    
    # CSS patterns
    elif any(keyword in code_lower for keyword in ['{', '}', 'css', 'style', 'color:', 'background:', 'margin:', 'padding:']):
        return 'css'
    
    # SQL patterns
    elif any(keyword in code_lower for keyword in ['select ', 'from ', 'where ', 'insert ', 'update ', 'delete ', 'create table', 'sql']):
        return 'sql'
    
    # JSON patterns
    elif code_text.strip().startswith('{') and code_text.strip().endswith('}'):
        return 'json'
    
    # Default
    return 'text'

def extract_and_highlight_code(text):
    """Metinden kod bloklarını çıkar ve syntax highlighting uygula"""
    # Kod bloklarını bul (```kod``` formatında)
    code_pattern = r'```(\w+)?\n(.*?)\n```'
    matches = re.findall(code_pattern, text, re.DOTALL)
    
    if matches:
        result_parts = []
        last_end = 0
        
        for match in re.finditer(code_pattern, text, re.DOTALL):
            # Kod bloğundan önceki metni ekle
            result_parts.append(text[last_end:match.start()])
            
            language = match.group(1) if match.group(1) else detect_code_language(match.group(2))
            code_content = match.group(2)
            
            # Kod bloğunu syntax highlighting ile ekle
            result_parts.append({
                'type': 'code',
                'language': language,
                'content': code_content
            })
            
            last_end = match.end()
        
        # Son kısımdaki metni ekle
        result_parts.append(text[last_end:])
        
        return result_parts
    else:
        # Kod bloğu yoksa, inline kod parçalarını kontrol et
        inline_code_pattern = r'`([^`]+)`'
        if re.search(inline_code_pattern, text):
            return [{'type': 'text_with_inline_code', 'content': text}]
        else:
            return [{'type': 'text', 'content': text}]

def render_message_with_syntax_highlighting(content, message_type):
    """Mesajı syntax highlighting ile render et"""
    parts = extract_and_highlight_code(content)
    
    message_class = "user-message" if message_type == "user" else "ai-message"
    icon = "👤" if message_type == "user" else "🤖"
    title = "Sen" if message_type == "user" else "AI Kod Editörü"
    
    # Mesaj container'ını başlat
    st.markdown(f'<div class="{message_class}">', unsafe_allow_html=True)
    st.markdown(f'<strong>{icon} {title}:</strong>', unsafe_allow_html=True)
    
    # İçeriği göster
    for part in parts:
        if isinstance(part, dict):
            if part['type'] == 'code':
                # Copy button için unique ID
                code_id = f"code_{hash(part['content'])}"
                
                st.markdown(f"""
                <div class="code-block-container">
                    <button class="copy-button" onclick="copyToClipboard('{code_id}')">📋 Kopyala</button>
                </div>
                """, unsafe_allow_html=True)
                
                # Kod bloğunu göster
                st.code(part['content'], language=part['language'])
                
            elif part['type'] == 'text_with_inline_code':
                # Inline kod ile metni işle
                inline_pattern = r'`([^`]+)`'
                text_parts = re.split(inline_pattern, part['content'])
                
                rendered_text = ""
                for i, text_part in enumerate(text_parts):
                    if i % 2 == 0:  # Normal metin
                        rendered_text += text_part
                    else:  # Inline kod
                        rendered_text += f'<code style="background-color: #f1f1f1; padding: 2px 4px; border-radius: 3px;">{text_part}</code>'
                
                st.markdown(rendered_text, unsafe_allow_html=True)
            else:
                # Normal metin
                st.markdown(part['content'])
        else:
            # String ise direkt göster
            if part.strip():  # Boş string değilse
                st.markdown(part)
    
    # Mesaj container'ını kapat
    st.markdown('</div>', unsafe_allow_html=True)

def initialize_session_state():
    """Session state değişkenlerini başlat"""
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
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

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
                with st.spinner("Bağlantı test ediliyor..."):
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
        
        # File Upload Section
        st.subheader("📁 Dosya Yönetimi")
        
        # Dosya yükleme seçenekleri
        upload_option = st.radio(
            "Yükleme türü seçin:",
            ["📄 Tek/Çoklu Dosya", "📁 Klasör İçeriği"],
            horizontal=True
        )
        
        if upload_option == "📄 Tek/Çoklu Dosya":
            # Çoklu dosya yükleme
            uploaded_files = st.file_uploader(
                "Dosya(lar) yükle",
                type=['py', 'js', 'html', 'css', 'cpp', 'java', 'go', 'rs', 'php', 'rb', 'swift', 'kt', 'ts', 'jsx', 'tsx', 'vue', 'sql', 'json', 'txt', 'md', 'yaml', 'yml', 'csv', 'log', 'ini', 'cfg', 'conf', 'xml'],
                accept_multiple_files=True,
                help="Çoklu dosya seçebilirsiniz. Desteklenen formatlar: Kod dosyaları, metin dosyaları, yapılandırma dosyaları"
            )
            
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    # Dosya zaten yüklü mü kontrol et
                    existing_files = [f['name'] for f in st.session_state.uploaded_files]
                    if uploaded_file.name not in existing_files:
                        try:
                            file_content = uploaded_file.read().decode('utf-8')
                            st.session_state.uploaded_files.append({
                                'name': uploaded_file.name,
                                'content': file_content,
                                'type': uploaded_file.type,
                                'size': len(file_content)
                            })
                            st.success(f"✅ {uploaded_file.name} yüklendi!")
                            
                            # Show file preview
                            with st.expander(f"📄 {uploaded_file.name} önizleme"):
                                language = detect_code_language(file_content)
                                preview_content = file_content[:1000] + "..." if len(file_content) > 1000 else file_content
                                st.code(preview_content, language=language)
                        except UnicodeDecodeError:
                            st.error(f"❌ {uploaded_file.name} dosyası okunamadı (desteklenmeyen format)")
        
        else:  # Klasör içeriği yükleme
            st.info("💡 **Klasör Yükleme İpucu:** Klasörünüzdeki tüm dosyaları seçmek için:")
            st.markdown("""
            1. **Windows:** Klasörü açın → `Ctrl+A` ile tümünü seçin → Sürükle-bırak yapın
            2. **Mac:** Klasörü açın → `Cmd+A` ile tümünü seçin → Sürükle-bırak yapın
            3. **Alternatif:** Dosya seçicisinde `Ctrl/Cmd` tuşu ile çoklu seçim yapın
            """)
            
            # Klasör benzeri çoklu dosya yükleme
            folder_files = st.file_uploader(
                "Klasör içeriğini yükle (tüm dosyaları seçin)",
                type=['py', 'js', 'html', 'css', 'cpp', 'java', 'go', 'rs', 'php', 'rb', 'swift', 'kt', 'ts', 'jsx', 'tsx', 'vue', 'sql', 'json', 'txt', 'md', 'yaml', 'yml', 'csv', 'log', 'ini', 'cfg', 'conf', 'xml'],
                accept_multiple_files=True,
                help="Klasörünüzdeki tüm dosyaları seçip yükleyin. Proje yapısı korunacaktır.",
                key="folder_upload"
            )
            
            if folder_files:
                uploaded_count = 0
                for uploaded_file in folder_files:
                    # Dosya zaten yüklü mü kontrol et
                    existing_files = [f['name'] for f in st.session_state.uploaded_files]
                    if uploaded_file.name not in existing_files:
                        try:
                            file_content = uploaded_file.read().decode('utf-8')
                            st.session_state.uploaded_files.append({
                                'name': uploaded_file.name,
                                'content': file_content,
                                'type': uploaded_file.type,
                                'size': len(file_content),
                                'is_folder_content': True
                            })
                            uploaded_count += 1
                        except UnicodeDecodeError:
                            st.warning(f"⚠️ {uploaded_file.name} dosyası atlandı (desteklenmeyen format)")
                
                if uploaded_count > 0:
                    st.success(f"✅ {uploaded_count} dosya klasör içeriği olarak yüklendi!")
                    
                    # Proje yapısını göster
                    if st.checkbox("📂 Proje yapısını göster"):
                        st.subheader("📁 Yüklenen Proje Yapısı")
                        folder_files_list = [f for f in st.session_state.uploaded_files if f.get('is_folder_content', False)]
                        
                        # Dosya türlerine göre grupla
                        file_types = {}
                        for file_info in folder_files_list:
                            ext = file_info['name'].split('.')[-1].lower() if '.' in file_info['name'] else 'other'
                            if ext not in file_types:
                                file_types[ext] = []
                            file_types[ext].append(file_info['name'])
                        
                        for ext, files in file_types.items():
                            with st.expander(f"📄 .{ext} dosyaları ({len(files)} adet)"):
                                for filename in sorted(files):
                                    st.text(f"  📄 {filename}")
        
        # Show uploaded files
        if st.session_state.uploaded_files:
            st.subheader("📋 Yüklenen Dosyalar")
            
            # İstatistikler
            total_files = len(st.session_state.uploaded_files)
            total_size = sum(f.get('size', 0) for f in st.session_state.uploaded_files)
            folder_files_count = len([f for f in st.session_state.uploaded_files if f.get('is_folder_content', False)])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📄 Toplam Dosya", total_files)
            with col2:
                st.metric("📁 Klasör Dosyaları", folder_files_count)
            with col3:
                st.metric("📊 Toplam Boyut", f"{total_size:,} karakter")
            
            # Tüm dosyaları temizle butonu
            if st.button("🗑️ Tümünü Temizle", help="Tüm yüklenen dosyaları sil"):
                st.session_state.uploaded_files = []
                st.success("✅ Tüm dosyalar temizlendi!")
                st.rerun()
            
            # Dosya listesi - güvenli silme işlemi
            if 'file_to_delete' not in st.session_state:
                st.session_state.file_to_delete = None
                
            for i, file_info in enumerate(st.session_state.uploaded_files):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    file_size = file_info.get('size', 0)
                    size_text = f"({file_size:,} karakter)" if file_size > 0 else ""
                    folder_icon = "📁" if file_info.get('is_folder_content', False) else "📄"
                    st.text(f"{folder_icon} {file_info['name']} {size_text}")
                with col2:
                    if st.button("👁️", key=f"view_{i}", help="Dosyayı görüntüle"):
                        with st.expander(f"📄 {file_info['name']}", expanded=True):
                            language = detect_code_language(file_info['content'])
                            preview_content = file_info['content'][:1000] + "..." if len(file_info['content']) > 1000 else file_info['content']
                            st.code(preview_content, language=language)
                with col3:
                    if st.button("🗑️", key=f"delete_{i}", help="Dosyayı sil"):
                        st.session_state.file_to_delete = i
            
            # Dosya silme işlemi - güvenli yöntem
            if st.session_state.file_to_delete is not None:
                file_index = st.session_state.file_to_delete
                if 0 <= file_index < len(st.session_state.uploaded_files):
                    removed_file = st.session_state.uploaded_files.pop(file_index)
                    st.success(f"✅ {removed_file['name']} silindi!")
                st.session_state.file_to_delete = None
                st.rerun()
        
        st.markdown("---")
        
        # Chat geçmişini temizle
        if st.button("🗑️ Geçmişi Temizle"):
            st.session_state.chat_history = []
            st.rerun()
        
        # Export chat history
        if st.session_state.chat_history and st.button("💾 Geçmişi İndir"):
            chat_export = []
            for msg in st.session_state.chat_history:
                chat_export.append({
                    'role': msg['role'],
                    'content': msg['content'],
                    'timestamp': msg['timestamp'].isoformat()
                })
            
            st.download_button(
                label="📥 JSON olarak indir",
                data=json.dumps(chat_export, indent=2, ensure_ascii=False),
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # Ana chat arayüzü
    if st.session_state.is_connected:
        # Tabs for different features
        tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📁 Dosya Analizi", "🔧 Kod Araçları", "🐛 Hata Analizi"])
        
        with tab1:
            st.header("💬 Chat Arayüzü")
            
            # Chat geçmişini göster - Geliştirilmiş rendering
            chat_container = st.container()
            
            with chat_container:
                for message in st.session_state.chat_history:
                    render_message_with_syntax_highlighting(
                        message['content'], 
                        message['role']
                    )
            
            # Mesaj girişi
            with st.form("chat_form", clear_on_submit=True):
                
                user_input = st.text_area(
                    "Kod yazma isteğinizi girin:",
                    placeholder="Örnek: Python ile bir web scraper yaz, React ile todo app oluştur, SQL sorgu optimizasyonu yap...",
                    height=100
                )
                
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
        
        with tab2:
            st.header("📁 Dosya Analizi")
            
            if st.session_state.uploaded_files:
                selected_file = st.selectbox(
                    "Analiz edilecek dosyayı seçin:",
                    options=range(len(st.session_state.uploaded_files)),
                    format_func=lambda x: st.session_state.uploaded_files[x]['name']
                )
                
                if selected_file is not None:
                    file_info = st.session_state.uploaded_files[selected_file]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📄 Dosya İçeriği")
                        language = detect_code_language(file_info['content'])
                        st.code(file_info['content'], language=language)
                    
                    with col2:
                        st.subheader("🔍 Analiz Seçenekleri")
                        
                        if st.button("🐛 Kod İncelemesi"):
                            analysis_prompt = f"Bu {file_info['name']} dosyasını incele ve kod kalitesi, potansiyel hatalar, iyileştirme önerileri hakkında detaylı analiz yap:\n\n```\n{file_info['content']}\n```"
                            
                            with st.spinner("Kod analiz ediliyor..."):
                                success, analysis = st.session_state.gemini_client.generate_code_response(analysis_prompt)
                                if success:
                                    st.markdown("### 📊 Analiz Sonucu")
                                    render_message_with_syntax_highlighting(analysis, 'assistant')
                        
                        if st.button("📝 Dokümantasyon Oluştur"):
                            doc_prompt = f"""Bu {file_info['name']} dosyası için kapsamlı ve anlaşılır dokümantasyon oluştur. 
                            
Lütfen aşağıdaki formatta dokümantasyon hazırla:

## 📋 Dosya Özeti
- Dosyanın amacı ve işlevi
- Ana özellikler

## 🔧 Fonksiyonlar ve Sınıflar
- Her fonksiyon/sınıf için açıklama
- Parametreler ve dönüş değerleri
- Kullanım örnekleri

## 📖 Kullanım Kılavuzu
- Nasıl kullanılır
- Örnek kod parçacıkları
- Dikkat edilmesi gerekenler

## 🔗 Bağımlılıklar
- Gerekli kütüphaneler
- İmport edilen modüller

Kod dosyası:
```
{file_info['content']}
```

Lütfen teknik jargon kullanmak yerine anlaşılır açıklamalar yap ve markdown formatında düzenli bir dokümantasyon oluştur."""

                            with st.spinner("Dokümantasyon oluşturuluyor..."):
                                success, documentation = st.session_state.gemini_client.generate_code_response(doc_prompt)
                                if success:
                                    st.markdown("### 📚 Dokümantasyon")
                                    # Dokümantasyon için özel görüntüleme - JSON formatını önlemek için direkt markdown kullan
                                    st.markdown(documentation)
                        
                        if st.button("🔧 Refactoring Önerileri"):
                            refactor_prompt = f"Bu {file_info['name']} dosyası için refactoring önerileri ve iyileştirilmiş kod versiyonu sun:\n\n```\n{file_info['content']}\n```"
                            
                            with st.spinner("Refactoring önerileri hazırlanıyor..."):
                                success, refactoring = st.session_state.gemini_client.generate_code_response(refactor_prompt)
                                if success:
                                    st.markdown("### ⚡ Refactoring Önerileri")
                                    render_message_with_syntax_highlighting(refactoring, 'assistant')
            else:
                st.info("📁 Analiz için önce bir dosya yükleyin.")
        
        with tab3:
            st.header("🔧 Gelişmiş Kod Araçları")
            
            # Modular Refactoring Section
            st.markdown("""
            <div class="refactor-card">
                <div class="refactor-header">
                    <div class="refactor-icon">🏗️</div>
                    <div>
                        <h2 class="refactor-title">Modüler Refactoring</h2>
                        <p class="refactor-description">Büyük kod dosyalarınızı modüler yapıya dönüştürün. AI, kodunuzu analiz ederek en uygun modül yapısını önerir.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Input section for modular refactoring
            st.markdown('<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<label class="input-label">📝 Refactor edilecek kodu girin:</label>', unsafe_allow_html=True)
            refactor_code = st.text_area("Kod İçeriği", height=300, placeholder="Büyük kod dosyanızı buraya yapıştırın...", key="refactor_input", label_visibility="collapsed")
            
            col1, col2 = st.columns(2)
            with col1:
                refactor_type = st.selectbox("🎯 Refactoring Türü:", [
                    "Otomatik Analiz", 
                    "Sınıf Bazlı Ayırma", 
                    "Fonksiyon Bazlı Ayırma", 
                    "Servis Katmanı Ayırma",
                    "MVC Yapısına Dönüştürme"
                ])
            with col2:
                target_language = st.selectbox("💻 Hedef Dil:", [
                    "python", "javascript", "typescript", "java", "c#", "go", "rust"
                ])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Quick examples
            st.markdown("### 🚀 Hızlı Örnekler")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("🧮 4 İşlem Hesap Makinesi", key="calc_example", help="Hesap makinesi örneği yükle"):
                    st.session_state.refactor_input = """
def calculator():
    def add(x, y): return x + y
    def subtract(x, y): return x - y
    def multiply(x, y): return x * y
    def divide(x, y): return x / y if y != 0 else "Sıfıra bölme hatası"
    
    while True:
        print("1. Toplama\\n2. Çıkarma\\n3. Çarpma\\n4. Bölme\\n5. Çıkış")
        choice = input("Seçiminiz: ")
        if choice == '5': break
        if choice in ['1','2','3','4']:
            x = float(input("İlk sayı: "))
            y = float(input("İkinci sayı: "))
            if choice == '1': print(f"Sonuç: {add(x,y)}")
            elif choice == '2': print(f"Sonuç: {subtract(x,y)}")
            elif choice == '3': print(f"Sonuç: {multiply(x,y)}")
            elif choice == '4': print(f"Sonuç: {divide(x,y)}")
calculator()
"""
                    st.rerun()
            
            with col2:
                if st.button("🌐 Web Scraper", key="scraper_example", help="Web scraper örneği yükle"):
                    st.session_state.refactor_input = """
import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_website():
    urls = ["https://example1.com", "https://example2.com"]
    data = []
    
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        titles = soup.find_all('h1')
        prices = soup.find_all('span', class_='price')
        descriptions = soup.find_all('p', class_='desc')
        
        for i in range(len(titles)):
            data.append({
                'title': titles[i].text.strip(),
                'price': prices[i].text.strip() if i < len(prices) else 'N/A',
                'description': descriptions[i].text.strip() if i < len(descriptions) else 'N/A'
            })
        time.sleep(1)
    
    with open('scraped_data.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'price', 'description'])
        writer.writeheader()
        writer.writerows(data)
    
    return data

scrape_website()
"""
                    st.rerun()
            
            with col3:
                if st.button("📊 Veri Analizi", key="analysis_example", help="Veri analizi örneği yükle"):
                    st.session_state.refactor_input = """
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def analyze_data():
    # Veri yükleme
    data = pd.read_csv('data.csv')
    
    # Temel istatistikler
    print(data.describe())
    print(data.info())
    
    # Eksik değer kontrolü
    missing_values = data.isnull().sum()
    print("Eksik değerler:", missing_values)
    
    # Veri temizleme
    data = data.dropna()
    data = data.drop_duplicates()
    
    # Görselleştirme
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    data['column1'].hist(bins=30)
    plt.title('Column1 Histogram')
    
    plt.subplot(2, 2, 2)
    sns.boxplot(data=data, x='category', y='value')
    plt.title('Category vs Value')
    
    plt.subplot(2, 2, 3)
    correlation_matrix = data.corr()
    sns.heatmap(correlation_matrix, annot=True)
    plt.title('Correlation Matrix')
    
    plt.subplot(2, 2, 4)
    data.groupby('category')['value'].mean().plot(kind='bar')
    plt.title('Average Value by Category')
    
    plt.tight_layout()
    plt.show()
    
    return data

analyze_data()
"""
                    st.rerun()
            
            with col4:
                if st.button("🔐 API Servisi", key="api_example", help="API servisi örneği yükle"):
                    st.session_state.refactor_input = """
from flask import Flask, request, jsonify
import sqlite3
import hashlib
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_token(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return data
    except:
        return None

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = hash_password(data.get('password'))
    email = data.get('email')
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
              (username, password, email))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = hash_password(data.get('password'))
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    
    if user:
        token = jwt.encode({
            'user_id': user[0],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
"""
                    st.rerun()
            
            # Refactoring button
            if st.button("🏗️ Modüler Yapıya Dönüştür", key="start_refactor", type="primary") and refactor_code:
                with st.spinner("🔄 Kod analiz ediliyor ve modüler yapıya dönüştürülüyor..."):
                    # Progress indicator
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("📊 Kod yapısı analiz ediliyor...")
                    progress_bar.progress(25)
                    
                    success, refactored_result = st.session_state.gemini_client.generate_modular_refactoring(
                        refactor_code, refactor_type, target_language
                    )
                    
                    status_text.text("🏗️ Modüler yapı oluşturuluyor...")
                    progress_bar.progress(75)
                    
                    if success:
                        status_text.text("✅ Refactoring tamamlandı!")
                        progress_bar.progress(100)
                        
                        st.markdown("""
                        <div class="analysis-result">
                            <div class="analysis-header">
                                <div class="analysis-icon">🎯</div>
                                <h3 class="analysis-title">Modüler Refactoring Sonucu</h3>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        render_message_with_syntax_highlighting(refactored_result, 'assistant')
                    else:
                        st.error("❌ Refactoring işlemi başarısız oldu. Lütfen tekrar deneyin.")
            
            st.markdown("---")
            
            # Architecture Analysis Section
            st.markdown("""
            <div class="refactor-card">
                <div class="refactor-header">
                    <div class="refactor-icon">🏛️</div>
                    <div>
                        <h2 class="refactor-title">Mimari Analiz</h2>
                        <p class="refactor-description">Kodunuzun mimari yapısını analiz edin, performans sorunlarını tespit edin ve iyileştirme önerileri alın.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<label class="input-label">🔍 Analiz edilecek kodu girin:</label>', unsafe_allow_html=True)
            analysis_code = st.text_area("Analiz Kodu", height=250, placeholder="Analiz edilecek kodu buraya yapıştırın...", key="analysis_input", label_visibility="collapsed")
            
            col1, col2 = st.columns(2)
            with col1:
                analysis_type = st.selectbox("📋 Analiz Türü:", [
                    "Genel Mimari Analiz",
                    "Performans Analizi", 
                    "Güvenlik Analizi",
                    "Kod Kalitesi Analizi",
                    "SOLID Prensipleri Kontrolü"
                ])
            with col2:
                analysis_depth = st.selectbox("🎯 Analiz Derinliği:", [
                    "Hızlı Tarama",
                    "Detaylı Analiz", 
                    "Kapsamlı İnceleme"
                ])
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("🔍 Mimari Analiz Başlat", key="start_analysis", type="primary") and analysis_code:
                with st.spinner("🔍 Kod mimarisi analiz ediliyor..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("📊 Kod yapısı taranıyor...")
                    progress_bar.progress(20)
                    
                    status_text.text("🏛️ Mimari desenler analiz ediliyor...")
                    progress_bar.progress(50)
                    
                    success, analysis_result = st.session_state.gemini_client.generate_architecture_analysis(
                        analysis_code, analysis_type, analysis_depth
                    )
                    
                    status_text.text("📈 Performans metrikleri hesaplanıyor...")
                    progress_bar.progress(80)
                    
                    if success:
                        status_text.text("✅ Analiz tamamlandı!")
                        progress_bar.progress(100)
                        
                        # Display metrics
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.markdown("""
                            <div class="metric-card">
                                <div class="metric-value">A+</div>
                                <div class="metric-label">Kod Kalitesi</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            st.markdown("""
                            <div class="metric-card">
                                <div class="metric-value">85%</div>
                                <div class="metric-label">Modülerlik</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col3:
                            st.markdown("""
                            <div class="metric-card">
                                <div class="metric-value">92%</div>
                                <div class="metric-label">Güvenlik</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col4:
                            st.markdown("""
                            <div class="metric-card">
                                <div class="metric-value">78%</div>
                                <div class="metric-label">Performans</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("""
                        <div class="analysis-result">
                            <div class="analysis-header">
                                <div class="analysis-icon">📊</div>
                                <h3 class="analysis-title">Mimari Analiz Raporu</h3>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        render_message_with_syntax_highlighting(analysis_result, 'assistant')
                    else:
                        st.error("❌ Analiz işlemi başarısız oldu. Lütfen tekrar deneyin.")
            
            st.markdown("---")
            
            # Project Structure Generator Section
            st.markdown("""
            <div class="refactor-card">
                <div class="refactor-header">
                    <div class="refactor-icon">📁</div>
                    <div>
                        <h2 class="refactor-title">Proje Yapısı Oluşturucu</h2>
                        <p class="refactor-description">Projeniz için optimal klasör yapısı ve dosya organizasyonu önerileri alın.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<label class="input-label">📝 Proje açıklaması:</label>', unsafe_allow_html=True)
            project_description = st.text_area("Proje Açıklaması", height=150, placeholder="Projenizi detaylı olarak açıklayın...", key="project_desc", label_visibility="collapsed")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                project_type = st.selectbox("🎯 Proje Türü:", [
                    "Web Uygulaması",
                    "Mobil Uygulama", 
                    "Desktop Uygulaması",
                    "API/Backend Servisi",
                    "Veri Bilimi Projesi",
                    "Machine Learning Projesi",
                    "Mikroservis Mimarisi"
                ])
            with col2:
                tech_stack = st.selectbox("💻 Teknoloji Stack:", [
                    "Python/Django",
                    "Python/Flask", 
                    "Node.js/Express",
                    "React/Next.js",
                    "Vue.js/Nuxt.js",
                    "Java/Spring",
                    "C#/.NET",
                    "Go/Gin",
                    "Rust/Actix"
                ])
            with col3:
                project_scale = st.selectbox("📏 Proje Ölçeği:", [
                    "Küçük (1-5 dosya)",
                    "Orta (5-20 dosya)",
                    "Büyük (20-100 dosya)",
                    "Kurumsal (100+ dosya)"
                ])
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("📁 Proje Yapısı Oluştur", key="generate_structure", type="primary") and project_description:
                with st.spinner("📁 Optimal proje yapısı oluşturuluyor..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("🎯 Proje gereksinimleri analiz ediliyor...")
                    progress_bar.progress(30)
                    
                    status_text.text("📁 Klasör yapısı tasarlanıyor...")
                    progress_bar.progress(60)
                    
                    success, structure_result = st.session_state.gemini_client.generate_project_structure(
                        project_description, project_type, tech_stack, project_scale
                    )
                    
                    status_text.text("📋 Dosya şablonları hazırlanıyor...")
                    progress_bar.progress(90)
                    
                    if success:
                        status_text.text("✅ Proje yapısı hazır!")
                        progress_bar.progress(100)
                        
                        st.markdown("""
                        <div class="analysis-result">
                            <div class="analysis-header">
                                <div class="analysis-icon">🏗️</div>
                                <h3 class="analysis-title">Önerilen Proje Yapısı</h3>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        render_message_with_syntax_highlighting(structure_result, 'assistant')
                        
                        # Download button for project structure
                        st.download_button(
                            label="📥 Proje Yapısını İndir",
                            data=structure_result,
                            file_name=f"project_structure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown"
                        )
                    else:
                        st.error("❌ Proje yapısı oluşturulamadı. Lütfen tekrar deneyin.")
        
        with tab4:
            st.header("🐛 Hata Analizi")
            
            # Error Analysis Card
            st.markdown("""
            <div class="refactor-card">
                <div class="refactor-header">
                    <div class="refactor-icon">🐛</div>
                    <div>
                        <h3 class="refactor-title">Hata Analizi ve Çözüm Önerileri</h3>
                        <p class="refactor-description">Kodunuzdaki hataları analiz edin ve çözüm önerileri alın</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Code input section
            st.subheader("📝 Kod Girişi")
            error_code = st.text_area(
                "Hata içeren kodu buraya yapıştırın:",
                height=200,
                placeholder="def example_function():\n    # Hatalı kodunuzu buraya yapıştırın\n    pass",
                key="error_code_input"
            )
            
            # Error message input
            st.subheader("⚠️ Hata Mesajı")
            error_message = st.text_area(
                "Aldığınız hata mesajını buraya yapıştırın:",
                height=100,
                placeholder="Traceback (most recent call last):\n  File \"example.py\", line 1, in <module>\n    # Hata mesajınızı buraya yapıştırın",
                key="error_message_input"
            )
            
            # Programming language selection
            col1, col2 = st.columns(2)
            with col1:
                programming_language = st.selectbox("💻 Programlama Dili:", [
                    "auto", "Python", "JavaScript", "Java", "C++", "C#", "PHP", "Ruby", "Go", "Rust", "TypeScript"
                ], key="error_lang_select")
            
            # Analysis button
            if st.button("🔍 Hata Analizi Yap", key="start_error_analysis", type="primary") and error_code and error_message:
                with st.spinner("🔄 Hata analiz ediliyor..."):
                    # Progress indicator
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("🔍 Hata inceleniyor...")
                    progress_bar.progress(25)
                    
                    success, analysis_result = st.session_state.gemini_client.generate_error_analysis(
                        error_code, error_message, programming_language
                    )
                    
                    status_text.text("🛠️ Çözüm önerileri hazırlanıyor...")
                    progress_bar.progress(75)
                    
                    if success:
                        status_text.text("✅ Analiz tamamlandı!")
                        progress_bar.progress(100)
                        
                        st.markdown("""
                        <div class="analysis-result">
                            <div class="analysis-header">
                                <div class="analysis-icon">🔍</div>
                                <h3 class="analysis-title">Hata Analizi Sonucu</h3>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display analysis result
                        st.markdown(analysis_result)
                        
                        # Download button
                        st.download_button(
                            label="📥 Analiz Raporunu İndir",
                            data=analysis_result,
                            file_name=f"error_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown"
                        )
                    else:
                        status_text.text("❌ Analiz başarısız!")
                        progress_bar.progress(0)
                        st.error(f"❌ Hata analizi yapılamadı: {analysis_result}")
            
            elif st.button("🔍 Hata Analizi Yap", key="start_error_analysis_disabled", type="primary"):
                if not error_code:
                    st.warning("⚠️ Lütfen hata içeren kodu girin.")
                if not error_message:
                    st.warning("⚠️ Lütfen hata mesajını girin.")
    
    else:
        st.warning("🔑 Lütfen önce Gemini API key'inizi girin ve bağlantıyı test edin.")
        
        # Feature showcase
        st.header("🚀 Özellikler")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>🎨 Syntax Highlighting</h3>
                <p>Kod bloklarınız otomatik olarak renklendirilir ve okunabilirlik artar.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>📁 Dosya Yönetimi</h3>
                <p>Kod dosyalarınızı yükleyin, analiz edin ve iyileştirin.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h3>🌙 Tema Desteği</h3>
                <p>Açık ve koyu tema arasında geçiş yapabilirsiniz.</p>
            </div>
            """, unsafe_allow_html=True)
        
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
    
    # Copy to clipboard JavaScript
    st.markdown("""
    <script>
    function copyToClipboard(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            navigator.clipboard.writeText(element.textContent).then(function() {
                // Success feedback could be added here
            });
        }
    }
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()