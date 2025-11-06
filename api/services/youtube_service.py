from googleapiclient.discovery import build # pyright: ignore[reportMissingImports]
import time

YOUTUBE_API_KEY = "AIzaSyDjjc5tFGYxn2U2iB2LGrR6-GGbuRSir2g"

def obtener_datos_video(video_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    req = youtube.videos().list(part="snippet,statistics", id=video_id)
    res = req.execute()
    if "items" in res and len(res["items"]) > 0:
        info = res["items"][0]
        titulo = info["snippet"]["title"]
        total = int(info["statistics"].get("commentCount", 0))
        return titulo, total
    return "No encontrado", 0


def obtener_comentarios(video_id, max_comments=200):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    comentarios = []
    token = None
    while True:
        try:
            req = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=token,
                textFormat="plainText"
            )
            res = req.execute()
            for item in res.get('items', []):
                comentario = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comentarios.append(comentario)
            token = res.get('nextPageToken')
            if not token or len(comentarios) >= max_comments:
                break
            time.sleep(0.2)
        except Exception as e:
            print("⚠️ Error al obtener comentarios:", e)
            break
    return comentarios
