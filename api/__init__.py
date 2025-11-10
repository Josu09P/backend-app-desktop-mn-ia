from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # CORS CONFIGURATION
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # IMPORT OF ROUTES
    from api.routes.youtube_routes import youtube_bp
    from api.routes.rl_multiple_routes import rl_multiple_bp
    from api.routes.rl_simple_routes import rl_simple_bp
    from api.routes.cluster_routes import cluster_bp
    from api.routes.face_auth_routes import face_auth_bp

    # REGISTER BLUEPRINTS
    app.register_blueprint(youtube_bp)
    app.register_blueprint(rl_multiple_bp)
    app.register_blueprint(rl_simple_bp)
    app.register_blueprint(cluster_bp, url_prefix="/api/cluster")
    app.register_blueprint(face_auth_bp)
    return app
