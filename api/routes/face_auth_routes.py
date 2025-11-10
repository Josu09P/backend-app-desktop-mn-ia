# api/routes/face_auth_routes.py
from flask import Blueprint, request, jsonify
import json, os
import numpy as np
from api.utils.token_manager import generate_token
from api.utils.face_processing import get_embedding_from_image_base64, calculate_face_distance
from api.utils.security import encrypt_embedding, decrypt_embedding
import base64

face_auth_bp = Blueprint("face_auth_bp", __name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "../db/users_db.json")

def load_users():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump([], f)
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_users(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)

# -------------------- REGISTRO FACIAL --------------------
# api/routes/face_auth_routes.py (parte del registro)
@face_auth_bp.route("/api/auth/facial/register", methods=["POST"])
def register_facial():
    data = request.get_json()
    user_id = data.get("user_id")
    image_data = data.get("image_base64")

    if not user_id or not image_data:
        return jsonify({
            "success": False,
            "message": "Datos incompletos"
        }), 400

    users = load_users()

    if any(u["user_id"] == user_id for u in users):
        return jsonify({
            "success": False,
            "message": "Usuario ya registrado"
        }), 400

    embedding = get_embedding_from_image_base64(image_data)
    if embedding is None:
        return jsonify({
            "success": False,
            "message": "No se detectó ningún rostro"
        }), 400

    # Asegurar que el embedding es numpy array
    embedding_array = np.array(embedding, dtype=np.float64)
    
    # Encriptar el embedding antes de guardar
    embedding_bytes = embedding_array.tobytes()
    encrypted_embedding = encrypt_embedding(embedding_bytes)
    encrypted_b64 = base64.b64encode(encrypted_embedding).decode('utf-8')

    token = generate_token(user_id)

    new_user = {
        "user_id": user_id,
        "embedding": encrypted_b64,  # Guardar encriptado como string base64
        "token": token
    }
    users.append(new_user)
    save_users(users)

    print(f"✅ Usuario {user_id} registrado. Total usuarios: {len(users)}")
    return jsonify({
        "success": True,
        "message": "Usuario registrado exitosamente", 
        "token": token
    }), 200

# -------------------- LOGIN FACIAL --------------------
# api/routes/face_auth_routes.py (SOLO la función login_facial)
@face_auth_bp.route("/api/auth/facial/login", methods=["POST"])
def login_facial():
    data = request.get_json()
    image_data = data.get("image_base64")

    if not image_data:
        return jsonify({
            "success": False,
            "message": "Imagen requerida"
        }), 400

    users = load_users()
    embedding_input = get_embedding_from_image_base64(image_data)

    if embedding_input is None:
        return jsonify({
            "success": False,
            "message": "No se detectó ningún rostro"
        }), 400

    # Buscar similitud con embeddings existentes
    for user in users:
        try:
            stored_embedding = None
            
            # FORMATO 1: Embedding encriptado (nuevo)
            if isinstance(user["embedding"], str) and len(user["embedding"]) > 100:
                try:
                    encrypted_bytes = base64.b64decode(user["embedding"])
                    decrypted_bytes = decrypt_embedding(encrypted_bytes)
                    stored_embedding = np.frombuffer(decrypted_bytes, dtype=np.float64)
                except Exception as e:
                    print(f"Error desencriptando usuario {user['user_id']}: {e}")
                    continue
                    
            # FORMATO 2: Embedding como lista (antiguo - compatibilidad)
            elif isinstance(user["embedding"], list):
                stored_embedding = np.array(user["embedding"], dtype=np.float64)
                
            else:
                print(f"Formato desconocido para usuario {user['user_id']}")
                continue
            
            # Calcular distancia si tenemos embedding válido
            if stored_embedding is not None:
                distance = calculate_face_distance(stored_embedding, embedding_input)
                print(f"🔍 Comparando con {user['user_id']}: distancia = {distance:.4f}")
                
                if distance < 0.6:  # Umbral típico
                    token = generate_token(user["user_id"])
                    print(f"✅ ACCESO CONCEDIDO: {user['user_id']} (distancia: {distance:.4f})")
                    return jsonify({
                        "success": True,
                        "message": "Acceso concedido",
                        "token": token,
                        "user_id": user["user_id"]
                    }), 200
                else:
                    print(f"❌ Distancia muy alta para {user['user_id']}: {distance:.4f}")
                    
        except Exception as e:
            print(f"Error procesando usuario {user['user_id']}: {e}")
            continue

    return jsonify({
        "success": False,
        "message": "No se reconoció ningún usuario"
    }), 401