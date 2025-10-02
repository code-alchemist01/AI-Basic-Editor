import subprocess
import sys
import os

def install_requirements():
    """Gerekli paketleri yükle"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Tüm paketler başarıyla yüklendi!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Paket yükleme hatası: {e}")
        return False

def run_app():
    """Uygulamayı çalıştır"""
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Uygulama kapatıldı!")
    except Exception as e:
        print(f"❌ Uygulama çalıştırma hatası: {e}")

if __name__ == "__main__":
    print("🚀 AI Kod Editörü başlatılıyor...")
    
    # Paketleri yükle
    if install_requirements():
        print("📱 Streamlit uygulaması başlatılıyor...")
        run_app()
    else:
        print("❌ Paket yükleme başarısız. Lütfen manuel olarak 'pip install -r requirements.txt' çalıştırın.")