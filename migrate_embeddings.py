# migrate_embeddings.py
import json
import os
import base64
import numpy as np
from api.utils.security import encrypt_embedding

DB_PATH = os.path.join(os.path.dirname(__file__), "api", "db", "users_db.json")

def migrate_embeddings():
    if not os.path.exists(DB_PATH):
        print("No se encontró la base de datos")
        return
    
    with open(DB_PATH, "r") as f:
        users = json.load(f)
    
    migrated_count = 0
    for user in users:
        # Si el embedding es una lista (formato antiguo), convertirlo
        if isinstance(user.get("embedding"), list):
            embedding_list = user["embedding"]
            # Convertir lista a numpy array y luego a bytes
            embedding_array = np.array(embedding_list, dtype=np.float64)
            embedding_bytes = embedding_array.tobytes()
            
            # Encriptar
            encrypted_embedding = encrypt_embedding(embedding_bytes)
            encrypted_b64 = base64.b64encode(encrypted_embedding).decode('utf-8')
            
            # Actualizar el usuario
            user["embedding"] = encrypted_b64
            migrated_count += 1
            print(f"✅ Migrado usuario: {user['user_id']}")
    
    if migrated_count > 0:
        # Guardar backup primero
        backup_path = DB_PATH + ".backup"
        with open(backup_path, "w") as f:
            json.dump(users, f, indent=2)
        print(f"✅ Backup guardado en: {backup_path}")
        
        # Guardar datos migrados
        with open(DB_PATH, "w") as f:
            json.dump(users, f, indent=2)
        print(f"✅ Migración completada: {migrated_count} usuarios actualizados")
    else:
        print("ℹ️ No se encontraron embeddings para migrar")

if __name__ == "__main__":
    migrate_embeddings()