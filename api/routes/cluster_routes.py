from flask import Blueprint, request, jsonify
import pandas as pd
from api.services.clustering_service import KMeansService

# ✅ NOMBRE CORRECTO DEL BLUEPRINT
cluster_bp = Blueprint("cluster", __name__)

@cluster_bp.route("/")
def home():
    return jsonify({"mensaje": "Backend de Clustering K-Means activo ✅"}), 200


@cluster_bp.route("/upload-csv", methods=["POST"])
def subir_csv():
    """Sube un CSV para trabajar con él"""
    if "file" not in request.files:
        return jsonify({"error": "Debes enviar un archivo CSV con la clave 'file'"}), 400
    
    archivo = request.files["file"]
    try:
        df = pd.read_csv(archivo)
        df.to_csv("data.csv", index=False)
        return jsonify({
            "filas": len(df),
            "columnas": list(df.columns)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cluster_bp.route("/kmeans/fit", methods=["POST"])
def entrenar_kmeans():
    """Entrena el modelo K-Means"""
    data = request.get_json() or {}
    features = data.get("features")
    n_clusters = data.get("n_clusters", 3)

    try:
        df = pd.read_csv("data.csv")
    except FileNotFoundError:
        return jsonify({"error": "Primero sube un CSV con /upload-csv"}), 400

    try:
        servicio = KMeansService(df)
        resultado = servicio.entrenar_modelo(features=features, n_clusters=n_clusters)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cluster_bp.route("/kmeans/predict", methods=["POST"])
def predecir_kmeans():
    """Predice el cluster de nuevas muestras"""
    datos = request.get_json()
    if not datos or "samples" not in datos:
        return jsonify({"error": "Debes enviar un JSON con la clave 'samples'"}), 400
    
    try:
        muestras = datos["samples"]
        servicio = KMeansService(pd.DataFrame())
        resultado = servicio.predecir_cluster(muestras)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
