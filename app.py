from flask import Flask, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "SyncGallery Backend OK"

@app.route("/files")
def files():

    import os

    return {
        "files": os.listdir("uploads")
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
