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
        return {"error": "No photo"}, 400

    file = request.files["photo"]

    os.makedirs("uploads", exist_ok=True)

    ruta = os.path.join(
        "uploads",
        file.filename
    )

    file.save(ruta)

    return {
        "ok": True,
        "archivo": file.filename
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
