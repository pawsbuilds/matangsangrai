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

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

for folder in [UPLOAD_FOLDER, RESULT_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024

MODEL_PATH = os.getenv("MODEL_PATH", "models/best.pt")
try:
    model = YOLO(MODEL_PATH)
    print(f"Berhasil load model: {MODEL_PATH}")
except Exception as e:
    print(f"FATAL: Gagal load model di {MODEL_PATH}. Error: {e}")

def manage_storage(folder_path):
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) 
             if os.path.isfile(os.path.join(folder_path, f)) and not f.startswith('.')]
    files.sort(key=os.path.getmtime)
    while len(files) > MAX_FILES:
        oldest_file = files.pop(0)
        try:
            os.remove(oldest_file)
            print(f"Cleanup: Menghapus {oldest_file}")
        except Exception as e:
            print(f"Error Cleanup: Gagal menghapus {oldest_file}: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('file')        
        if file and file.filename != '' and allowed_file(file.filename):
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

            manage_storage(app.config['UPLOAD_FOLDER'])
            manage_storage(app.config['RESULT_FOLDER'])

            return render_template("index.html", result_image=f"results/{result_filename}", original_image=f"uploads/{unique_name}", items=items)

    return render_template("index.html", result_image=None, original_image=None, items=[])

@app.route("/cron/cleanup", methods=["GET"])
def cron_cleanup():
    cron_key = os.getenv("CRON_SECRET_KEY")
    auth_key = request.args.get("key")

    if not cron_key or auth_key != cron_key:
        return "Unauthorized", 403

    try:
        manage_storage(app.config['UPLOAD_FOLDER'])
        manage_storage(app.config['RESULT_FOLDER'])
        return "Cleanup Success", 200
    except Exception as e:
        return f"Cleanup Failed: {str(e)}", 500

if __name__ == "__main__":
    from waitress import serve
    
    port = int(os.environ.get("PORT", 7860))

    print(f"Server MatangSangrai aktif di port {port}")
    serve(app, host='0.0.0.0', port=port)