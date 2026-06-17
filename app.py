from flask import Flask, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "SyncGallery Backend OK"

@app.route("/upload", methods=["POST"])
def upload():

    if "photo" not in request.files:
        return {"error": "no photo"}, 400

    file = request.files["photo"]

    ruta = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(ruta)

    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
