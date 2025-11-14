from flask import Blueprint, request, jsonify # type: ignore
import pandas as pd # pyright: ignore[reportMissingModuleSource]
from api.services.clustering_service import KMeansService

cluster_bp = Blueprint("cluster", __name__)

@cluster_bp.route("/")
def home():
    return jsonify({"mensaje": "Backend de Clustering K-Means activo ✅"}), 200


@cluster_bp.route("/kmeans/fit", methods=["POST"])
def entrenar_kmeans():
    data = request.get_json() or {}
    
    raw_data_list = data.get("data") 
    features = data.get("features")
    n_clusters = data.get("n_clusters", 3)

    if not raw_data_list:
        return jsonify({"error": "Debes enviar los datos de entrenamiento con la clave 'data'"}), 400

    try:
        servicio = KMeansService(pd.DataFrame()) 
        resultado = servicio.entrenar_modelo(
            features=features, 
            n_clusters=n_clusters,
            raw_data_list=raw_data_list 
        )
        return jsonify(resultado), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


@cluster_bp.route("/kmeans/predict", methods=["POST"])
def predecir_kmeans():
    datos = request.get_json()
    if not datos or "samples" not in datos:
        return jsonify({"error": "Debes enviar un JSON con la clave 'samples'"}), 400
    
    try:
        muestras = datos["samples"]
        
        servicio = KMeansService(pd.DataFrame())
        resultado = servicio.predecir_cluster(muestras)
        return jsonify(resultado), 200
    except FileNotFoundError:
        return jsonify({"error": "El modelo K-Means no ha sido entrenado. Ejecuta /kmeans/fit primero."}), 400
    except Exception as e:
        return jsonify({"error": f"Error al predecir: {str(e)}"}), 500