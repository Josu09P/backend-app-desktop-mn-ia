from flask import Blueprint, request, jsonify
from datetime import datetime
from api.services.youtube_service import obtener_datos_video, obtener_comentarios
from api.utils.sentiment import clasificar_sentimiento
import pandas as pd
from api.utils.keywords import obtener_palabras_clave
youtube_bp = Blueprint("youtube", __name__, url_prefix="/api")


@youtube_bp.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response


@youtube_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"OK, Laburando desde ya mi lord...": True, "timestamp": datetime.now().isoformat()})

@youtube_bp.route("/analizar", methods=["POST"])
def analizar():
    body = request.get_json()
    url = body.get("url", "").strip()
    max_comments = int(body.get("max_comments", 200))

    if not url:
        return jsonify({"error": "Debes enviar una URL"}), 400

    # ✅ Limpieza del video_id
    if "v=" in url:
        video_id = url.split("v=")[-1].split("&")[0].split("?")[0]
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1].split("?")[0]
    else:
        return jsonify({"error": "URL inválida"}), 400

    # ✅ Obtener datos del video
    datos_video = obtener_datos_video(video_id)
    if not datos_video:
        return jsonify({"error": "No se encontraron datos del video"}), 404

    # ✅ Obtener comentarios
    comentarios = obtener_comentarios(video_id, max_comments=max_comments) 
    if not comentarios:
        return jsonify({"error": "No se encontraron comentarios para analizar"}), 404

    # ✅ Análisis de sentimientos
    resultados = [clasificar_sentimiento(c) for c in comentarios]
    df = pd.DataFrame({"Comentario": comentarios, "Sentimiento": resultados})
    conteo = df["Sentimiento"].value_counts().to_dict()

    # ✅ Análisis de Palabras Clave
    palabras_clave = obtener_palabras_clave(comentarios, top_n=15) # Obtener las 15 más comunes

    # ✅ Respuesta completa
    return jsonify({
        **datos_video,
        "total_comentarios": len(comentarios), # Este es el número ANALIZADO
        "conteo": conteo,
        "palabras_clave": palabras_clave,
        "resultados": df.to_dict(orient="records")
    })