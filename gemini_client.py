import google.generativeai as genai
import streamlit as st

class GeminiClient:
    def __init__(self):
        self.model = None
        self.is_connected = False
    
    def connect(self, api_key, model_name="gemini-2.0-flash"):
        """Gemini API'ye bağlan"""
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)
            
            # Bağlantıyı test et
            test_response = self.model.generate_content("Test")
            self.is_connected = True
            return True, "Bağlantı başarılı!"
        except Exception as e:
            self.is_connected = False
            return False, f"Bağlantı hatası: {e}"
    
    def generate_code_response(self, user_prompt):
        """Kod editörü için optimize edilmiş prompt ile yanıt üret"""
        
        expert_prompt = f"""
Sen uzman bir AI kod editörüsün. Görevin kullanıcının isteklerine göre en iyi kodu yazmak ve kod problemlerini çözmek.

UZMANLIK ALANLARIN:
- Python, JavaScript, TypeScript, Java, C#, C++, Go, Rust, PHP
- Web geliştirme (React, Vue, Angular, Node.js, Django, Flask)
- Mobil geliştirme (React Native, Flutter, Swift, Kotlin)
- Veritabanı (SQL, NoSQL, ORM'ler)
- DevOps ve Cloud (Docker, Kubernetes, AWS, Azure, GCP)
- Makine öğrenmesi ve AI
- Algoritma ve veri yapıları

YANIT KURALLARIN:
1. Her zaman çalışan, temiz ve optimize kod yaz
2. Kod açıklamalarını Türkçe yap
3. Best practice'leri takip et
4. Güvenlik açıklarına dikkat et
5. Performance optimizasyonu yap
6. Error handling ekle
7. Gerekirse test kodları da yaz

KULLANICI İSTEĞİ:
{user_prompt}

Lütfen bu isteği en profesyonel şekilde karşıla ve detaylı açıklamalarla birlikte kod örnekleri ver.
"""
        
        try:
            response = self.model.generate_content(expert_prompt)
            return True, response.text
        except Exception as e:
            return False, f"Yanıt üretme hatası: {e}"
    
    def get_token_count(self, text):
        """Token sayısını hesapla (yaklaşık)"""
        try:
            return len(text.split()) * 1.3  # Yaklaşık hesaplama
        except:
            return 0