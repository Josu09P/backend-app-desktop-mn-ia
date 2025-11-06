from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # ✅ Configuración CORS abierta (solo para desarrollo)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Importar y registrar las rutas
    from api.routes.youtube_routes import youtube_bp
    app.register_blueprint(youtube_bp)

    return app
