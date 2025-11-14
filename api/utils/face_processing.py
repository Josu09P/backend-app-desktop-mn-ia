import numpy as np
import face_recognition
from PIL import Image
import io
import base64
import os
from ultralytics import YOLO 

# --- CONFIGURACIÓN DE RUTAS ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'best.pt')
YOLO_MODEL = None

def load_yolo_model():
    """
    Carga el modelo YOLO (best.pt) para la detección de rostros.
    """
    global YOLO_MODEL
    try:
        YOLO_MODEL = YOLO(MODEL_PATH)
        print(f"INFO: Modelo YOLO cargado desde: {MODEL_PATH}")
        print("INFO: Modelo de Embedding (FaceNet) de 'face_recognition' listo.")
        return True 
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo del modelo en {MODEL_PATH}")
        print("Asegúrate de que 'best.pt' está en api/models/.")
        YOLO_MODEL = None
        return False
    except Exception as e:
        print(f"ERROR: Fallo al cargar el modelo YOLO: {e}")
        YOLO_MODEL = None
        return False

# Cargar el modelo al inicio
load_yolo_model()
# ---------------------------------------------


def get_embedding_from_image_base64(image_base64: str) -> np.ndarray | None:
    """
    Decodifica la imagen Base64, usa YOLO para DETECCIÓN y FaceNet para EMBEDDING.
    """
    if YOLO_MODEL is None:
        print("ERROR: El modelo YOLO no está disponible.")
        return None
        
    try:
        # 1. Decodificar la imagen
        image_bytes = base64.b64decode(image_base64)
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        rgb_array = np.array(pil_image)
        
        # 2. Detección del Rostro con YOLO
        # 'results' contiene los bounding boxes de los rostros detectados.
        # mode='predict' es la forma de hacer inferencia en YOLOv8/v5
        results = YOLO_MODEL.predict(rgb_array, verbose=False)
        
        face_locations = []
        if results and len(results) > 0:
            # Iterar sobre las detecciones para obtener las coordenadas
            # Formato de YOLO: [x1, y1, x2, y2, confidence, class_id]
            for detection in results[0].boxes.data.tolist():
                x1, y1, x2, y2, conf, cls = detection
                
                # Convertir formato YOLO (x1, y1, x2, y2) a formato dlib (top, right, bottom, left)
                # Face-recognition (dlib) espera enteros
                top = int(y1)
                right = int(x2)
                bottom = int(y2)
                left = int(x1)
                face_locations.append((top, right, bottom, left))

        if len(face_locations) == 0:
            return None # No se encontró ningún rostro
        
        if len(face_locations) > 1:
            # Para el login, se requiere solo un rostro.
            print("ADVERTENCIA: Múltiples rostros detectados. Usando el primer rostro.")
        
        # 3. Generación del Embedding (Usando FaceNet en base al recuadro detectado)
        # face_recognition necesita la imagen original y los 'face_locations' para extraer la huella.
        embeddings = face_recognition.face_encodings(rgb_array, face_locations)
        
        if len(embeddings) > 0:
            return embeddings[0] # Devolver el primer embedding
        else:
            return None
            
    except Exception as e:
        print(f"Error durante el procesamiento facial: {e}")
        return None


def calculate_face_distance(embedding_a: np.ndarray, embedding_b: np.ndarray) -> float:
    """Calcula la distancia de la cara entre dos embeddings (Distancia Euclidiana)."""
    try:
        # Asegurar que ambos son numpy arrays del mismo tipo
        embedding_a = np.array(embedding_a, dtype=np.float64)
        embedding_b = np.array(embedding_b, dtype=np.float64)
        
        # Verificar dimensiones
        if embedding_a.shape != embedding_b.shape:
            print(f"Dimensiones diferentes: {embedding_a.shape} vs {embedding_b.shape}")
            return 1.0
            
        distances = face_recognition.face_distance([embedding_a], embedding_b)
        if len(distances) > 0:
            return float(distances[0])
        return 1.0
    except Exception as e:
        print(f"Error calculando distancia facial: {e}")
        return 1.0