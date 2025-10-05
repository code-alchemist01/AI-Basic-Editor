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
        
        # Eğer prompt dokümantasyon oluşturma ile ilgiliyse, özel bir yaklaşım kullan
        if "dokümantasyon" in user_prompt.lower() or "documentation" in user_prompt.lower():
            expert_prompt = f"""
Sen uzman bir teknik yazardın ve kod dokümantasyonu konusunda uzmansın. Görevin verilen kodu analiz edip anlaşılır, kullanıcı dostu dokümantasyon oluşturmak.

DOKÜMANTASYON PRENSİPLERİN:
1. Teknik jargon yerine anlaşılır dil kullan
2. Örneklerle açıkla
3. Adım adım kılavuzlar hazırla
4. Görsel düzen için markdown formatı kullan
5. Kullanıcının seviyesine uygun açıklamalar yap

KULLANICI İSTEĞİ:
{user_prompt}

Lütfen bu isteği karşılarken, kod hakkında sadece teknik detaylar vermek yerine, kullanıcının kodu nasıl kullanabileceği, ne işe yaradığı ve nasıl çalıştığı hakkında pratik bilgiler ver.
"""
        else:
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
Sen uzman bir yazılım mimarısı ve kod danışmanısın. Görevin verilen kodu analiz edip kullanıcıya modüler yapıya dönüştürme konusunda pratik rehberlik etmek.

REFACTORING TİPİ: {refactoring_type}
DOSYA ADI: {file_name}

YAKLAŞIMIN:
- Açıklayıcı metinler ağırlıklı olsun ama teknik detayları da dahil et
- Anlaşılır dil kullan, gerektiğinde teknik terimleri açıkla
- Pratik adımlar ve öneriler ver
- Kod örnekleri minimal ama öğretici olsun
- Neden bu değişikliklerin gerekli olduğunu açıkla

## 🔍 KOD ANALİZ RAPORU

### 📊 Mevcut Durum
Kodunuz şu anda [değerlendirme] durumda. İşte tespit ettiğim ana noktalar:

**📏 Kod Büyüklüğü:** [X] satır kod
**🎯 Ana Sorumluluklar:** 
- [Sorumluluk 1]: Ne yaptığı ve neden ayrılması gerektiği
- [Sorumluluk 2]: Ne yaptığı ve neden ayrılması gerektiği
- [Sorumluluk 3]: Ne yaptığı ve neden ayrılması gerektiği

**⚠️ Tespit Edilen Sorunlar:**
- [Sorun 1]: Neden problem olduğu ve nasıl çözüleceği
- [Sorun 2]: Neden problem olduğu ve nasıl çözüleceği

**🔧 Teknik Değerlendirme:**
- **Coupling (Bağımlılık):** [Yüksek/Orta/Düşük] - [Açıklama]
- **Cohesion (İç Tutarlılık):** [Yüksek/Orta/Düşük] - [Açıklama]
- **Complexity (Karmaşıklık):** [Yüksek/Orta/Düşük] - [Açıklama]

### 🏗️ ÖNERİLEN MODÜLER YAPI

**📁 Klasör Organizasyonu:**
```
proje-adi/
├── 📄 main.py              # Ana çalıştırma dosyası
├── 📁 core/                # Temel işlevler
│   ├── 📄 [modül1].py      # [Açıklama]
│   └── 📄 [modül2].py      # [Açıklama]
├── 📁 utils/               # Yardımcı fonksiyonlar
│   └── 📄 helpers.py       # [Açıklama]
└── 📁 config/              # Ayar dosyaları
    └── 📄 settings.py      # [Açıklama]
```

### 💡 MODÜL AÇIKLAMALARI

**🔧 [Modül 1 Adı]**
- **Ne yapar:** [Açık açıklama]
- **Neden ayrı olmalı:** [Sebep]
- **İçereceği fonksiyonlar:** [Liste]
- **Diğer modüllerle ilişkisi:** [Açıklama]
- **Teknik detay:** [Interface/API tasarımı, veri yapıları]

**🔧 [Modül 2 Adı]**
- **Ne yapar:** [Açık açıklama]
- **Neden ayrı olmalı:** [Sebep]
- **İçereceği fonksiyonlar:** [Liste]
- **Diğer modüllerle ilişkisi:** [Açıklama]
- **Teknik detay:** [Interface/API tasarımı, veri yapıları]

### 🚀 UYGULAMA REHBERİ

#### 1️⃣ Hazırlık Aşaması (5-10 dakika)
- **Adım 1:** [Açık talimat]
- **Adım 2:** [Açık talimat]
- **Adım 3:** [Açık talimat]

#### 2️⃣ Modül Oluşturma (15-30 dakika)
- **[Modül 1] için:** [Hangi kodları taşıyacağı ve nasıl]
  - *Teknik not:* [Import yapısı, dependency injection vb.]
- **[Modül 2] için:** [Hangi kodları taşıyacağı ve nasıl]
  - *Teknik not:* [Error handling, logging vb.]
- **Ana dosya için:** [Ne kalacağı ve nasıl düzenleneceği]

#### 3️⃣ Bağlantıları Kurma (10-15 dakika)
- **Import yapısı:** [Hangi dosyaların birbirini import edeceği]
- **Veri akışı:** [Modüller arası veri nasıl geçecek]
- **Test etme:** [Nasıl kontrol edileceği]
- **Teknik kontroller:** [Type hints, docstrings, error handling]

### 🔍 ÖRNEK KOD YAPISI
Kritik noktalar için minimal kod örnekleri:

**Modül Interface Örneği:**
```python
# [Modül adı] için temel yapı
class [ModuleName]:
    def __init__(self, config):
        # Temel kurulum
    
    def main_method(self, data):
        # Ana işlev
        return result
```

### ✅ FAYDALAR
Bu modüler yapıya geçtikten sonra:
- **Kod okunabilirliği:** [Nasıl artacağı]
- **Bakım kolaylığı:** [Nasıl kolaylaşacağı]
- **Yeniden kullanım:** [Hangi parçalar tekrar kullanılabilir]
- **Hata ayıklama:** [Nasıl kolaylaşacağı]
- **Test edilebilirlik:** [Unit test yazma kolaylığı]
- **Performans:** [Lazy loading, caching olanakları]

### 🎯 SONRAKİ ADIMLAR
1. **Hemen yapılabilecekler:** [Basit başlangıç adımları]
2. **Bu hafta içinde:** [Orta vadeli hedefler]
3. **Gelecek planlar:** [Uzun vadeli iyileştirmeler]

ANALİZ EDİLECEK KOD:
{code_content}

Lütfen kodu analiz ederken açıklayıcı metinleri ağırlıklı tut ama teknik detayları da dengeli şekilde ekle. Kullanıcı hem anlasın hem de teknik derinliği görsün.
"""
        
        try:
            response = self.model.generate_content(refactoring_prompt)
            return True, response.text
        except Exception as e:
            return False, f"Modüler refactoring hatası: {e}"
    
    def generate_architecture_analysis(self, code_content, analysis_type="full", analysis_depth="medium"):
        """Kod mimarisini analiz et ve iyileştirme önerileri sun"""
        
        analysis_prompt = f"""
Sen uzman bir yazılım mimarısı ve kod danışmanısın. Görevin verilen kodu kullanıcı dostu bir şekilde analiz edip pratik öneriler sunmak.

ANALİZ TİPİ: {analysis_type}
ANALİZ DERİNLİĞİ: {analysis_depth}

YAKLAŞIMIN:
- Teknik terimler yerine anlaşılır açıklamalar kullan
- Somut örneklerle açıkla
- Pratik çözümler öner
- Adım adım rehberlik et
- Kullanıcının seviyesine uygun dil kullan
- Markdown formatını doğru kullan

YAPILACAK ANALİZLER:
1. Kod Yapısı ve Organizasyon
2. Kod Kalitesi ve Okunabilirlik  
3. Performans ve Verimlilik
4. Güvenlik ve Hata Yönetimi
5. Test Edilebilirlik
6. Geliştirilebilirlik
7. Bakım ve Sürdürülebilirlik

ÇIKTI FORMATI:

## 📊 KOD ANALİZ RAPORU

### 🎯 GENEL DURUM
Bu kodunuz genel olarak [değerlendirme] durumda. İşte öne çıkan noktalar:

**✅ İyi Yanlar:**
- [Pozitif nokta 1]: Neden iyi olduğu
- [Pozitif nokta 2]: Neden iyi olduğu

**⚠️ Geliştirilmesi Gerekenler:**
- [İyileştirme alanı 1]: Neden önemli olduğu
- [İyileştirme alanı 2]: Neden önemli olduğu

### 🔍 DETAYLI İNCELEME

#### 📋 Kod Organizasyonu
[Kodun nasıl düzenlendiği hakkında anlaşılır açıklama]

#### 🎯 Performans Durumu  
[Kodun hızı ve verimliliği hakkında pratik bilgiler]

#### 🛡️ Güvenlik ve Hata Yönetimi
[Güvenlik açıkları ve hata durumları hakkında açıklama]

### 💡 PRATİK ÖNERİLER

#### 🚀 Hemen Yapılabilecekler (1-2 gün)
1. **[Öneri 1]**
   - Ne yapılacak: [Açıklama]
   - Neden önemli: [Sebep]
   - Nasıl yapılır: [Adımlar]

2. **[Öneri 2]**
   - Ne yapılacak: [Açıklama]
   - Neden önemli: [Sebep]
   - Nasıl yapılır: [Adımlar]

#### 📈 Orta Vadeli İyileştirmeler (1-2 hafta)
1. **[Öneri 1]**: [Açıklama ve faydası]
2. **[Öneri 2]**: [Açıklama ve faydası]

#### 🎯 Uzun Vadeli Hedefler (1+ ay)
1. **[Hedef 1]**: [Açıklama ve neden önemli]
2. **[Hedef 2]**: [Açıklama ve neden önemli]

### 📚 KAYNAK VE ARAÇLAR
- [Önerilen araç/kaynak 1]: Neden faydalı
- [Önerilen araç/kaynak 2]: Neden faydalı

ANALİZ EDİLECEK KOD:
{code_content}

Lütfen kodu analiz ederken kullanıcının anlayabileceği bir dil kullan ve pratik, uygulanabilir öneriler sun. Markdown formatını doğru kullan ve kod blokları yerine açıklayıcı metinler tercih et.
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
    
    def generate_error_analysis(self, code_content, error_message, programming_language="auto"):
        """Hata analizi ve çözüm önerileri oluştur"""
        
        error_analysis_prompt = f"""
Sen deneyimli bir yazılım geliştirici ve hata ayıklama uzmanısın. Verilen kod ve hata mesajını analiz ederek kapsamlı bir hata analizi raporu hazırla.

YAKLAŞIMIN:
- Anlaşılır ve pratik açıklamalar yap
- Teknik terimleri açıkla
- Adım adım çözüm önerileri sun
- Benzer hataları önleme yollarını belirt

KOD:
```
{code_content}
```

HATA MESAJI:
{error_message}

PROGRAMLAMA DİLİ: {programming_language}

Lütfen aşağıdaki formatta bir analiz raporu hazırla:

## 🔍 HATA ANALİZİ RAPORU

### 📋 Hata Özeti
- **Hata Türü:** [Hata kategorisi]
- **Önem Derecesi:** [Kritik/Yüksek/Orta/Düşük]
- **Etkilenen Alan:** [Hangi kod bölümü]

### 🎯 Olası Nedenler
1. **Ana Neden:** [En olası sebep]
2. **İkincil Nedenler:** [Diğer olasılıklar]
3. **Çevresel Faktörler:** [Sistem, kütüphane versiyonları vb.]

### 🛠️ Çözüm Adımları
1. **Hızlı Çözüm:** [Acil durum için]
2. **Kalıcı Çözüm:** [Uzun vadeli]
3. **Test Etme:** [Çözümü doğrulama]

### 💡 Önleme Önerileri
- **Kod Kalitesi:** [İyi pratikler]
- **Test Stratejisi:** [Nasıl test edilmeli]
- **Monitoring:** [İzleme önerileri]

### 🔧 Örnek Düzeltme
[Gerekirse minimal kod örneği]

### 📚 Ek Kaynaklar
- **Dokümantasyon:** [İlgili kaynaklar]
- **Benzer Durumlar:** [Yaygın hatalar]
"""
        
        try:
            response = self.model.generate_content(error_analysis_prompt)
            return True, response.text
        except Exception as e:
            return False, f"Hata analizi hatası: {e}"