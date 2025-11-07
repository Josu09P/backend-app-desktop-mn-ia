from googleapiclient.discovery import build # pyright: ignore[reportMissingImports]
import time

# Usa tu clave de API
YOUTUBE_API_KEY = "AIzaSyDjjc5tFGYxn2U2iB2LGrR6-GGbuRSir2g" 

def obtener_datos_video(video_id):
    """Obtiene el título, canal, fecha, miniatura y estadísticas del video."""
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    req = youtube.videos().list(part="snippet,statistics", id=video_id)
    res = req.execute()

    if "items" in res and len(res["items"]) > 0:
        info = res["items"][0]
        snippet = info["snippet"]
        stats = info["statistics"]

        return {
            "titulo": snippet["title"],
            "canal": snippet["channelTitle"],
            "fecha_publicacion": snippet["publishedAt"],
            "miniatura": snippet["thumbnails"]["medium"]["url"],
            "likes": int(stats.get("likeCount", 0)),
            "vistas": int(stats.get("viewCount", 0)),
            "total_comentarios_video": int(stats.get("commentCount", 0))
        }

    return None

def obtener_comentarios(video_id, max_comments=200):
    """
    Obtiene hasta 'max_comments' de un video de YouTube.
    Itera usando el nextPageToken para superar el límite de 100 comentarios por solicitud.
    """
    
    # Si max_comments es cero o negativo, no hacemos la llamada
    if max_comments <= 0:
        return []

    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    comentarios = []
    token = None
    
    while True:
        # Si ya alcanzamos el límite deseado, salimos.
        if len(comentarios) >= max_comments:
            break
            
        # Calcula cuántos resultados pedir en esta página (máximo 100)
        remaining_to_fetch = max_comments - len(comentarios)
        page_size = min(100, remaining_to_fetch)

        try:
            req = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=page_size,
                pageToken=token,
                textFormat="plainText"
            )
            res = req.execute()
            
            for item in res.get('items', []):
                comentario = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comentarios.append(comentario)
                
            token = res.get('nextPageToken')

            # Si no hay más páginas (token es None), salimos.
            if not token:
                break
                
            # Pequeña pausa para no saturar la API.
            time.sleep(0.2) 
            
        except Exception as e:
            print("⚠️ Error al obtener comentarios:", e)
            break
            
    # Devolvemos solo la cantidad solicitada (esto es redundante si la lógica del loop funciona bien, pero es una buena práctica de seguridad)
    return comentarios[:max_comments]