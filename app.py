USERNAME = "ivan"
PASSWORD = "123456ivan"
from flask import (
    Flask,
    request,
    send_from_directory,
    Response
)
import os
def check_auth(username, password):

    return (
        username == USERNAME and
        password == PASSWORD
    )


def authenticate():

    return Response(
        "Login requerido",
        401,
        {
            "WWW-Authenticate":
            'Basic realm="SyncGallery"'
        }
    )


def requires_auth(f):

    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):

        auth = request.authorization

        if (
            not auth or
            not check_auth(
                auth.username,
                auth.password
            )
        ):
            return authenticate()

        return f(*args, **kwargs)

    return decorated
    
app = Flask(__name__)

PHOTOS_FOLDER = "uploads/photos"
VIDEOS_FOLDER = "uploads/videos"

os.makedirs(PHOTOS_FOLDER, exist_ok=True)
os.makedirs(VIDEOS_FOLDER, exist_ok=True)

@app.route("/")
@requires_auth
def home():

    fotos = os.listdir(PHOTOS_FOLDER)
    videos = os.listdir(VIDEOS_FOLDER)
    total_fotos = len(fotos)
    total_videos = len(videos)
    html = """
    <html>
    <head>
        <title>SyncGallery</title>
        <style>
            body {
                font-family: Arial;
                background: #111;
                color: white;
                padding: 20px;
            }

            img {
                width: 200px;
                margin: 10px;
                border-radius: 10px;
            }

            video {
                width: 300px;
                margin: 10px;
                border-radius: 10px;
            }

            .galeria {
                display: flex;
                flex-wrap: wrap;
            }
        </style>
    </head>
    <body>

        <h1>📷 SyncGallery</h1>

        <h2>Fotos</h2>
        <h3>
            Fotos: """ + str(total_fotos) + """
            &nbsp;&nbsp;|&nbsp;&nbsp;
            Videos: """ + str(total_videos) + """
        </h3>
        <a href="/clear">
    <button>
        🗑 Limpiar Todo
    </button>
</a>

<br><br>
        <div class="galeria">
    """

    for foto in fotos:

        html += f'''
<div>

<a href="/photo/{foto}" target="_blank">
    <img src="/photo/{foto}">
</a>

<br>

<a href="/delete/photo/{foto}">
    <button>🗑 Borrar</button>
</a>

</div>
'''

    html += """
        </div>

        <h2>🎥 Videos</h2>

        <div class="galeria">
    """

    for video in videos:

       html += f'''
<div>

<video controls>
    <source src="/video/{video}">
</video>

<br>

<a href="/delete/video/{video}">
    <button>🗑 Borrar</button>
</a>

</div>
'''

    html += """
        </div>

    </body>
    </html>
    """

    return html
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
@requires_auth
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
@requires_auth
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
@requires_auth
def photo(filename):

    return send_from_directory(
        PHOTOS_FOLDER,
        filename
    )
@app.route("/video/<filename>")
@requires_auth
def video(filename):

    return send_from_directory(
        VIDEOS_FOLDER,
        filename
    )
    
@app.route("/delete/photo/<filename>")
@requires_auth
def delete_photo(filename):

    ruta = os.path.join(
        PHOTOS_FOLDER,
        filename
    )

    if os.path.exists(ruta):
        os.remove(ruta)

    return """
    <script>
    window.location='/'
    </script>
    """
@app.route("/delete/video/<filename>")
@requires_auth
def delete_video(filename):

    ruta = os.path.join(
        VIDEOS_FOLDER,
        filename
    )

    if os.path.exists(ruta):
        os.remove(ruta)

    return """
    <script>
    window.location='/'
    </script>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
