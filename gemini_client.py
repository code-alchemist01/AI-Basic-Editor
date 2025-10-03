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
    
    def generate_modular_refactoring(self, code_content, file_name="", refactoring_type="auto"):
        """Monolitik kodu modüler yapıya dönüştür"""
        
        refactoring_prompt = f"""
Sen uzman bir yazılım mimarısın. Görevin verilen monolitik kodu analiz edip modüler bir yapıya dönüştürmek.

REFACTORING TİPİ: {refactoring_type}
DOSYA ADI: {file_name}

GÖREVLER:
1. Kodu analiz et ve sorumlulukları belirle
2. Uygun modüllere/sınıflara ayır
3. Her modül için ayrı dosya öner
4. Klasör yapısını tasarla
5. Import/export yapısını kur
6. Ana dosyayı (main.py/index.js) oluştur

ÇIKTI FORMATI:
```
## 📊 KOD ANALİZİ
- Toplam satır sayısı: X
- Tespit edilen sorumluluklar: [liste]
- Önerilen modül sayısı: X

## 📁 ÖNERİLEN KLASÖR YAPISI
```
proje/
├── main.py
├── modules/
│   ├── __init__.py
│   ├── module1.py
│   └── module2.py
└── utils/
    └── helpers.py
```

## 🔧 MODÜLLER

### 📄 main.py
```python
# Ana dosya kodu
```

### 📄 modules/module1.py
```python
# Modül 1 kodu
```

## 🔗 ENTEGRASYON REHBERİ
1. Dosyaları oluştur
2. Kodları kopyala
3. Test et
```

REFACTOR EDİLECEK KOD:
{code_content}

Lütfen kodu profesyonel bir şekilde modüler yapıya dönüştür ve detaylı açıklamalar ver.
"""
        
        try:
            response = self.model.generate_content(refactoring_prompt)
            return True, response.text
        except Exception as e:
            return False, f"Modüler refactoring hatası: {e}"
    
    def generate_architecture_analysis(self, code_content, analysis_type="full", analysis_depth="medium"):
        """Kod mimarisini analiz et ve iyileştirme önerileri sun"""
        
        analysis_prompt = f"""
Sen uzman bir yazılım mimarısın. Görevin verilen kodu derinlemesine analiz edip mimari iyileştirmeler önermek.

ANALİZ TİPİ: {analysis_type}
ANALİZ DERİNLİĞİ: {analysis_depth}

YAPILACAK ANALİZLER:
1. 🏗️ Mimari Kalite Analizi
2. 🔍 Kod Kalitesi Değerlendirmesi  
3. 🚀 Performance Analizi
4. 🔒 Güvenlik Değerlendirmesi
5. 🧪 Test Edilebilirlik
6. 📈 Ölçeklenebilirlik
7. 🔧 Bakım Kolaylığı

ÇIKTI FORMATI:
```
## 📊 MİMARİ ANALİZ RAPORU

### 🎯 GENEL DEĞERLENDIRME
- Mimari Kalite Puanı: X/10
- Kod Kalitesi: X/10
- Bakım Kolaylığı: X/10

### 🔍 TESPİT EDİLEN SORUNLAR
#### 🚨 Kritik Sorunlar
- [Sorun 1]: Açıklama ve çözüm önerisi
- [Sorun 2]: Açıklama ve çözüm önerisi

#### ⚠️ Orta Seviye Sorunlar
- [Sorun 1]: Açıklama ve çözüm önerisi

#### 💡 İyileştirme Önerileri
- [Öneri 1]: Detaylı açıklama
- [Öneri 2]: Detaylı açıklama

### 🏗️ ÖNERİLEN MİMARİ
```python
# Önerilen mimari yapı örneği
```

### 📋 UYGULAMA PLANI
1. **Kısa Vadeli (1-2 hafta)**
   - [Görev 1]
   - [Görev 2]

2. **Orta Vadeli (1-2 ay)**
   - [Görev 1]
   - [Görev 2]

3. **Uzun Vadeli (3+ ay)**
   - [Görev 1]
   - [Görev 2]
```

ANALİZ EDİLECEK KOD:
{code_content}

Lütfen kodu detaylı analiz et ve profesyonel öneriler sun.
"""
        
        try:
            response = self.model.generate_content(analysis_prompt)
            return True, response.text
        except Exception as e:
            return False, f"Mimari analiz hatası: {e}"
    
    def generate_project_structure(self, project_description, project_type="web", tech_stack="", project_scale="medium"):
        """Proje açıklamasına göre optimal klasör yapısı oluştur"""
        
        structure_prompt = f"""
Sen uzman bir yazılım mimarısın. Görevin verilen proje açıklamasına göre sadece optimal klasör yapısı ve dosya organizasyonu oluşturmak.

PROJE TİPİ: {project_type}
TEKNOLOJİ STACK: {tech_stack}
PROJE ÖLÇEĞİ: {project_scale}

PROJE AÇIKLAMASI:
{project_description}

ÖNEMLİ: Sadece proje yapısını göster. Kurulum talimatları, README içeriği veya detaylı açıklamalar ekleme.

ÇIKTI FORMATI (sadece bu kısmı üret):
```
## 📁 PROJE YAPISI

```
proje-adi/
│
├── 📁 backend/                       # Backend uygulaması
│   │
│   ├── 📁 apps/                      # Django uygulamaları
│   │   ├── 📁 users/                 # Kullanıcı yönetimi
│   │   │   ├── 📄 models.py
│   │   │   ├── 📄 views.py
│   │   │   ├── 📄 serializers.py
│   │   │   └── 📄 urls.py
│   │   │
│   │   ├── 📁 products/              # Ürün yönetimi
│   │   │   ├── 📄 models.py
│   │   │   ├── 📄 views.py
│   │   │   ├── 📄 serializers.py
│   │   │   └── 📄 urls.py
│   │   │
│   │   └── 📁 orders/                # Sipariş yönetimi
│   │       ├── 📄 models.py
│   │       ├── 📄 views.py
│   │       ├── 📄 serializers.py
│   │       └── 📄 urls.py
│   │
│   ├── 📁 config/                    # Django ayarları
│   │   ├── 📄 settings.py
│   │   ├── 📄 urls.py
│   │   └── 📄 wsgi.py
│   │
│   ├── 📄 manage.py                  # Django yönetim dosyası
│   └── 📄 requirements.txt           # Python bağımlılıkları
│
├── 📁 frontend/                      # React frontend
│   │
│   ├── 📁 src/                       # Kaynak kodlar
│   │   ├── 📁 components/            # React bileşenleri
│   │   │   ├── 📄 Header.jsx
│   │   │   ├── 📄 Footer.jsx
│   │   │   └── 📄 ProductCard.jsx
│   │   │
│   │   ├── 📁 pages/                 # Sayfa bileşenleri
│   │   │   ├── 📄 Home.jsx
│   │   │   ├── 📄 Products.jsx
│   │   │   └── 📄 Cart.jsx
│   │   │
│   │   ├── 📁 services/              # API servisleri
│   │   │   └── 📄 api.js
│   │   │
│   │   ├── 📄 App.jsx                # Ana uygulama
│   │   └── 📄 main.jsx               # Giriş noktası
│   │
│   ├── 📄 package.json               # Node.js bağımlılıkları
│   ├── 📄 vite.config.js             # Vite konfigürasyonu
│   └── 📄 index.html                 # Ana HTML dosyası
│
├── 📄 .env.example                   # Çevre değişkenleri örneği
├── 📄 .gitignore                     # Git ignore kuralları
├── 📄 README.md                      # Proje açıklaması
└── 📄 docker-compose.yml             # Docker konfigürasyonu
```
```

Bu proje için optimal yapıyı tasarla. Sadece klasör yapısını göster, başka hiçbir şey ekleme.
"""
        
        try:
            response = self.model.generate_content(structure_prompt)
            return True, response.text
        except Exception as e:
            return False, f"Proje yapısı oluşturma hatası: {e}"