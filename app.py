import os
import uuid
import cv2
from flask import Flask, render_template, request, session, redirect, url_for
from ultralytics import YOLO
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_key_do_not_use_in_prod")

UPLOAD_FOLDER = os.path.join('static', 'uploads')
RESULT_FOLDER = os.path.join('static', 'results')
MAX_FILES = int(os.getenv("MAX_FILES", 10))

for folder in [UPLOAD_FOLDER, RESULT_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

MODEL_PATH = ("models/best.pt")
model = YOLO(MODEL_PATH)

def manage_storage(folder_path):
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) 
             if os.path.isfile(os.path.join(folder_path, f))]
    files.sort(key=os.path.getmtime)
    while len(files) > MAX_FILES:
        oldest_file = files.pop(0)
        try:
            os.remove(oldest_file)
        except Exception as e:
            print(f"Gagal menghapus {oldest_file}: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('file')        
        if file and file.filename != '':
            ext = os.path.splitext(file.filename)[1]
            unique_name = f"{uuid.uuid4().hex[:8]}{ext}"
            
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            file.save(img_path)

            results = model.predict(
                source=img_path, 
                save=False, 
                conf=0.25
            )

            res_plotted = results[0].plot()
            result_filename = f"result_{unique_name.split('.')[0]}.jpg"
            result_save_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
            cv2.imwrite(result_save_path, res_plotted)

            items = []
            if len(results[0].boxes) > 0:
                class_ids = results[0].boxes.cls.cpu().tolist()
                items = list(set([results[0].names[int(id)] for id in class_ids]))

            session['result_data'] = {
                'result_image' : f"results/{result_filename}",
                'original_image' : f"uploads/{unique_name}",
                'items' : items
            }

            manage_storage(app.config['UPLOAD_FOLDER'])
            manage_storage(app.config['RESULT_FOLDER'])

            return redirect(url_for('index'))
    
    data = session.pop('result_data', None)

    if data:
        return render_template("index.html", result_image=data['result_image'], original_image=data['original_image'], items=data['items'])
    
    return render_template("index.html", result_image=None, original_image=None, items=[])

# Tambahkan ini di bagian route app.py
@app.route("/cron/cleanup", methods=["GET"])
def cron_cleanup():
    # Ambil API Key dari .env untuk keamanan
    cron_key = os.getenv("CRON_SECRET_KEY")
    auth_key = request.args.get("key")

    # Validasi: Hanya jalankan jika key sesuai
    if auth_key != cron_key:
        return "Unauthorized", 403

    try:
        # Jalankan fungsi pembersihan yang sudah kita buat sebelumnya
        manage_storage(app.config['UPLOAD_FOLDER'])
        manage_storage(app.config['RESULT_FOLDER'])
        return "Cleanup Success", 200
    except Exception as e:
        return f"Cleanup Failed: {str(e)}", 500

if __name__ == "__main__":
    env = os.getenv("ENV", "development")

    if env == "production":
        from waitress import serve
        print("MatangSangrai running on PRODUCTION (Waitress Port 5000)")
        serve(app, host='0.0.0.0', port=5000)

    else:
        try:
            from livereload import Server
            print("Running on DEVELOPMENT (LiveReload)")
            server = Server(app.wsgi_app)
            server.watch('static/css/*.css')
            server.watch('static/js/*.js')
            server.watch('templates/*.html')
            server.serve(port=5000, debug=True)
        except ImportError:
            print("Running on DEVELOPMENT (Standard Flask)")
            app.run(debug=True, port=5000)