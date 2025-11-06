from flask import Blueprint, request, jsonify
from datetime import datetime
from api.services.youtube_service import obtener_datos_video, obtener_comentarios
from api.utils.sentiment import clasificar_sentimiento
import pandas as pd # pyright: ignore[reportMissingModuleSource]

youtube_bp = Blueprint("youtube", __name__, url_prefix="/api")

@youtube_bp.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response


@youtube_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "timestamp": datetime.now().isoformat()})


@youtube_bp.route("/analizar", methods=["POST"])
def analizar():
    body = request.get_json()
    url = body.get("url", "").strip()

    if not url:
        return jsonify({"error": "Debes enviar una URL"}), 400

    # Extraer el ID del video
    if "v=" in url:
        video_id = url.split("v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1]
    else:
        return jsonify({"error": "URL inválida"}), 400

    # Obtener datos del video y comentarios
    titulo, total = obtener_datos_video(video_id)
    comentarios = obtener_comentarios(video_id)
    if not comentarios:
        return jsonify({"error": "No se encontraron comentarios"}), 404

    resultados = [clasificar_sentimiento(c) for c in comentarios]
    df = pd.DataFrame({'Comentario': comentarios, 'Sentimiento': resultados})
    conteo = df['Sentimiento'].value_counts().to_dict()

    return jsonify({
        "titulo_video": titulo,
        "total_comentarios": len(comentarios),
        "total_comentarios_video": total,
        "conteo": conteo,
        "resultados": df.to_dict(orient="records")
    })
