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

    fotos = len(os.listdir(PHOTOS_FOLDER))
    videos = len(os.listdir(VIDEOS_FOLDER))

    return f"""
    <html>
    <body style="
        font-family:Arial;
        text-align:center;
        margin-top:50px;
    ">

    <h1>📷 SyncGallery</h1>

    <h2>
        Fotos: {fotos}
        <br>
        Videos: {videos}
    </h2>

    <br>

    <a href="/photos">
        <button>
            📸 Fotos
        </button>
    </a>

    <br><br>

    <a href="/videos">
        <button>
            🎥 Videos
        </button>
    </a>

    <br><br>

    <a href="/clear">
        <button>
            🗑 Limpiar Todo
        </button>
    </a>

    </body>
    </html>
    """
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

@app.route("/photos")
@requires_auth
def photos():

    fotos = os.listdir(PHOTOS_FOLDER)

   html = """
<html>
<body style="
    font-family:Arial;
    background:#111;
    color:white;
">

<h1 style="text-align:center;">
📸 Fotos
</h1>

<div style="
    display:grid;
    grid-template-columns:
        repeat(auto-fill,minmax(250px,1fr));
    gap:20px;
    padding:20px;
">
"""

    for foto in fotos:

       html += f"""
<div style="
    background:#222;
    padding:10px;
    border-radius:10px;
    text-align:center;
">

    <a href="/photo/{foto}" target="_blank">
        <img
            src="/photo/{foto}"
            style="
                width:100%;
                height:250px;
                object-fit:cover;
                border-radius:10px;
            "
        >
    </a>

    <br><br>

    <a href="/delete/photo/{foto}">
        <button>
            🗑 Borrar
        </button>
    </a>

</div>
"""

    html += "</body></html>"

    return html

@app.route("/videos")
@requires_auth
def videos():

    videos = os.listdir(VIDEOS_FOLDER)

   html = """
<html>
<body style="
    font-family:Arial;
    background:#111;
    color:white;
">

<h1 style="text-align:center;">
📸 videos
</h1>

<div style="
    display:grid;
    grid-template-columns:
        repeat(auto-fill,minmax(250px,1fr));
    gap:20px;
    padding:20px;
">
"""

    for video in videos:

        html += f"""
<div style="
    background:#222;
    padding:10px;
    border-radius:10px;
    text-align:center;
">

    <video
        controls
        style="
            width:100%;
            height:250px;
            object-fit:cover;
            border-radius:10px;
        "
    >
        <source src="/video/{video}">
    </video>

    <br><br>

    <a href="/delete/video/{video}">
        <button>
            🗑 Borrar
        </button>
    </a>

</div>
"""

    html += "</body></html>"

    return html


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
   window.location='/photos'
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
    window.location='/videos'
    </script>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
