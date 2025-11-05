from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Importar y registrar las rutas
    from api.routes.youtube_routes import youtube_bp
    app.register_blueprint(youtube_bp)

    return app
