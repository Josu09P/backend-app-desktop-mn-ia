from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # ✅ Configuración CORS abierta (solo para desarrollo)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Importar y registrar las rutas
    from api.routes.youtube_routes import youtube_bp
    from api.routes.rl_multiple_routes import rl_multiple_bp
    from api.routes.cluster_routes import cluster_bp
    app.register_blueprint(youtube_bp)
    app.register_blueprint(rl_multiple_bp)
    app.register_blueprint(cluster_bp, url_prefix="/api/cluster")
    return app
