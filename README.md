# Org-Flask Mini API for Service Booking

![Python](https://img.shields.io/badge/python-3.11-blue.svg)

Bu proje, bir teknik değerlendirme görevi kapsamında geliştirilmiş, basit bir etkinlik hizmeti listeleme ve rezervasyon talebi alma API'sidir. Proje, sadece temel gereksinimleri karşılamakla kalmaz, aynı zamanda modern yazılım geliştirme pratikleri, modüler mimari, sağlam hata yönetimi, loglama ve otomatik testler gibi profesyonel özellikleri de içerir.

## ✨ Temel Özellikler

- **RESTful API Endpoints:** Hizmetleri listelemek (`GET`) ve yeni rezervasyon talepleri oluşturmak (`POST`) için iki ana endpoint.
- **Detaylı Veri Doğrulama (Validation):**
  - Gerekli alanların (`service_ids`, `event_date`) kontrolü.
  - Veri tiplerinin doğrulanması (`service_ids` bir liste olmalıdır).
  - Tarih formatının (`YYYY-MM-DD`) ve geçmiş bir tarih olmamasının kontrolü.
- **Gelişmiş Mantıksal Doğrulama:**
  - Gönderilen `service_ids` içindeki her bir ID'nin sistemde gerçekten var olup olmadığının kontrolü.
  - Aynı rezervasyon talebinde bir hizmetin birden fazla kez eklenmesini (tekrarlanan ID'ler) engelleme.
- **Profesyonel Proje Mimarisi:**
  - **Flask Blueprints** kullanılarak kodun `services` ve `bookings` gibi mantıksal modüllere ayrılması.
  - "Application Factory" deseni (`create_app`) ile yapılandırılabilir ve test edilebilir bir uygulama yapısı.
- **Gelişmiş Loglama:**
  - Hem **terminale** hem de ayrı bir **`logs/` klasöründeki dosyaya** loglama.
  - Başarılı isteklerin, uyarıların ve hataların detaylı (gelen veri dahil) loglanması.
  - Türkçe karakterleri destekleyen **UTF-8** formatında log kaydı.
- **Otomatik Test Altyapısı:**
  - **Pytest** ile yazılmış kapsamlı birim testleri.
  - Başarılı senaryolar ("Happy Path") ve tüm hatalı durumlar (geçersiz ID, geçmiş tarih, tekrar eden ID vb.) için test senaryoları.
- **Bonus: İnteraktif Test Arayüzü:**
  - **Gradio** ile geliştirilmiş, API'yi test etmek için kullanıcı dostu bir web arayüzü.

## 📂 Proje Yapısı

Proje, ölçeklenebilir ve yönetilebilir bir yapıda organize edilmiştir:

```
org-flask/
├── app/
│   ├── __init__.py         # Application Factory ve loglama yapılandırması
│   ├── models.py           # Hardcoded verilerin tutulduğu modül
│   ├── services.py         # Hizmetler (services) için Blueprint
│   └── bookings.py         # Rezervasyonlar (bookings) için Blueprint
├── logs/
│   └── org-flask-api.log     # Log kayıtlarının tutulduğu dosya
├── tests/
│   └── test_api.py         # Pytest birim testleri
├── venv/
├── .gitignore              # Git tarafından takip edilmeyecek dosyalar
├── README.md               # Bu dosya
├── requirements.txt        # Proje bağımlılıkları
├── pytest.ini              # Pytest yapılandırma dosyası
├── run.py                  # Flask uygulamasını başlatan script
└── ui_tester.py            # Gradio ile geliştirilen interaktif test arayüzü
```

## 🛠️ Kullanılan Teknolojiler

- **Backend:** Flask
- **Test:** Pytest
- **Test Arayüzü:** Gradio
- **HTTP İstekleri (UI Tester için):** Requests

## 🚀 Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

### 1. Projeyi Klonlama

```powershell
git clone https://github.com/habipokc/org-flask.git
cd org-flask
```

### 2. Sanal Ortam Oluşturma ve Aktifleştirme

```powershell
# Sanal ortamı oluştur
python -m venv venv

# Sanal ortamı aktifleştir (PowerShell)
.\venv\Scripts\Activate.ps1
```

### 3. Bağımlılıkları Yükleme

```powershell
pip install -r requirements.txt
```

### 4. API Sunucusunu Başlatma

API sunucusu, tüm endpoint'lerin çalışması için arka planda aktif olmalıdır.

```powershell
python run.py
```
Sunucu varsayılan olarak `http://127.0.0.1:5000` adresinde çalışmaya başlayacaktır.

### 5. Otomatik Testleri Çalıştırma

Projenin tüm fonksiyonlarının doğru çalıştığını doğrulamak için:

```powershell
pytest
```
Tüm testlerin (`5 passed`) başarıyla geçtiğini görmelisiniz.

## 📖 API Endpointleri

### 1. Hizmetleri Listeleme

- **Endpoint:** `GET /api/v1/services`
- **Açıklama:** Sistemde mevcut olan tüm hizmetleri listeler.
- **Başarılı Yanıt (200 OK):**
  ```json
  [
    {
      "id": 1,
      "name": "DJ Hizmeti (2 Saat)",
      "category": "Müzik & Sanatçı",
      "price": 5000
    },
    {
      "id": 2,
      "name": "Masa Süsleme (Romantik)",
      "category": "Dekorasyon & Süsleme",
      "price": 1500
    }
  ]
  ```

### 2. Rezervasyon Talebi Oluşturma

- **Endpoint:** `POST /api/v1/bookings`
- **Açıklama:** Yeni bir rezervasyon talebi oluşturur.
- **İstek Gövdesi (Request Body):**
  ```json
  {
    "service_ids":,
    "event_date": "2025-12-24",
    "notes": "Yılbaşı kutlaması için özel bir istek."
  }
  ```
- **Başarılı Yanıt (201 Created):**
  ```json
  {
    "message": "Rezervasyon talebiniz alındı.",
    "booking_id": 5678
  }
  ```
- **Hatalı Yanıtlar (400 Bad Request):**
  - _Eksik veya yanlış formatta tarih:_
    ```json
    {
      "error": "Geçersiz veri.",
      "details": {
        "event_date": "Tarih formatı YYYY-MM-DD olmalıdır."
      }
    }
    ```
  - _Geçersiz hizmet ID'si:_
    ```json
    {
      "error": "Geçersiz veri.",
      "details": {
        "service_ids": "Geçersiz hizmet ID'si: 99. Bu ID sistemde mevcut değil."
      }
    }
    ```

## 💡 Bonus: İnteraktif UI Tester

Komut satırı araçları kullanmadan API'yi kolayca test etmek için bir web arayüzü geliştirilmiştir.

**Çalıştırma:**
1.  API sunucusunun çalıştığından emin olun (`python run.py`).
2.  **Yeni bir terminal** açın, sanal ortamı aktifleştirin ve aşağıdaki komutu çalıştırın:
    ```powershell
    python ui_tester.py
    ```
3.  Tarayıcınızda `http://127.0.0.1:7860` adresine gidin ve API'yi test etmeye başlayın!