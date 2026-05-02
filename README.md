# MatangSangrai
MatangSangrai adalah aplikasi berbasis web yang menggunakan model **YOLOv12** untuk mendeteksi dan mengklasifikasikan tingkat kematangan sangrai biji kopi (*Roasting Levels*) secara otomatis. Proyek ini dikembangkan menggunakan **Flask** sebagai backend dan mendukung deteksi melalui unggahan gambar.

## Fitur Utama
- Deteksi otomatis tingkat kematangan: Raw, Light, Medium, dan Dark Roast.
- Manajemen penyimpanan otomatis.
- Antarmuka responsif dengan Tailwind CSS.
- Arsitektur siap produksi menggunakan Waitress WSGI.

## Teknologi
- **Python 3.10+**
- **Flask**: Web Framework.
- **YOLOv12**: Object Detection Model.
- **OpenCV**: Image Processing.
- **Tailwind CSS**: Styling.

## Instalasi

1. **Clone Repositori**
   git clone [https://github.com/pawbuilds/matangsangrai.git](https://github.com/username/matangsangrai.git)
   cd matangsangrai

2. **Buat Virtual Environment**
    python -m venv venv
    source venv/bin/scripts/activate  # Untuk Windows: venv\Scripts\activate

3. **Instal Dependensi**
    pip install -r requirements.txt
4. **Konfigurasi Environment**
    FLASK_SECRET_KEY=your_secret_key_here
    ENV=development
    MAX_FILES=10
    MODEL_PATH=models/best.pt

## Cara Menjalankan
    python app.py
