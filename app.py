from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

PHOTOS_FOLDER = "uploads/photos"
VIDEOS_FOLDER = "uploads/videos"

os.makedirs(PHOTOS_FOLDER, exist_ok=True)
os.makedirs(VIDEOS_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "SyncGallery Backend OK"
@app.route("/upload", methods=["POST"])
def upload():

    if "photo" not in request.files:
        return {"error": "No file"}, 400

    file = request.files["photo"]

    nombre = file.filename.lower()

    if nombre.endswith(".mp4"):

        ruta = os.path.join(
            VIDEOS_FOLDER,
            file.filename
        )

    else:

        ruta = os.path.join(
            PHOTOS_FOLDER,
            file.filename
        )

    file.save(ruta)

    return {
        "ok": True,
        "archivo": file.filename
    }

@app.route("/clear")
def clear():

    for carpeta in [
        PHOTOS_FOLDER,
        VIDEOS_FOLDER
    ]:

        for archivo in os.listdir(carpeta):

            ruta = os.path.join(
                carpeta,
                archivo
            )

            os.remove(ruta)

    return {"ok": True}

@app.route("/files")
def files():

    return {
        "photos": os.listdir(
            PHOTOS_FOLDER
        ),
        "videos": os.listdir(
            VIDEOS_FOLDER
        )
    }
@app.route("/photo/<filename>")
def photo(filename):

    return send_from_directory(
        PHOTOS_FOLDER,
        filename
    )
@app.route("/video/<filename>")
def video(filename):

    return send_from_directory(
        VIDEOS_FOLDER,
        filename
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
