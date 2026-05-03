---
title: MatangSangrai
emoji: ☕
colorFrom: yellow
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

# MatangSangrai
MatangSangrai adalah aplikasi berbasis web yang menggunakan model **YOLOv12** untuk mendeteksi dan mengklasifikasikan tingkat kematangan sangrai biji kopi (*Roasting Levels*) secara otomatis. Proyek ini dikembangkan menggunakan **Flask** sebagai backend dan mendukung deteksi melalui unggahan gambar.

## Fitur Utama
- Deteksi otomatis tingkat kematangan: Raw, Light, Medium, dan Dark Roast.
- Manajemen penyimpanan otomatis.
- Interface responsif dengan Tailwind CSS.
- Arsitektur siap produksi menggunakan Waitress WSGI.

## Teknologi
- **Python 3.10+**
- **Flask**: Web Framework.
- **YOLOv12**: Object Detection Model.
- **OpenCV**: Image Processing.
- **Tailwind CSS**: Styling.

## Instalasi

1. **Clone Repositori**
   git clone [https://github.com/pawbuilds/matangsangrai.git](https://github.com/pawsbuilds/matangsangrai.git)
   cd matangsangrai

2. **Buat Virtual Environment**
    python -m venv venv
    Linux/MacOs: source venv/bin/activate  
    Windows: venv\Scripts\activate

3. **Instal Dependensi**
    pip install -r requirements.txt
4. **Konfigurasi Environment**
    FLASK_SECRET_KEY=your_secret_key_here
    ENV=development
    MAX_FILES=10
    MODEL_PATH=models/best.pt
    CRON_SECRET_KEY=cron_secret_key_here

## Cara Menjalankan
    python app.py
