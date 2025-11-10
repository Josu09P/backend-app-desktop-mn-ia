from cryptography.fernet import Fernet
import os

ENCRYPTION_KEY = os.environ.get(
    "FACE_ENCRYPTION_KEY", 
    "uY4E6cQG0WbX9RjVpI5zL7kF2hT8mN1o3sA4dJ6yH9gC7qP2fE0wXvU3tY8sZ1xR6"
).encode() # Convertir a bytes para Fernet

try:
    # Inicializa la suite de cifrado con la clave
    cipher_suite = Fernet(ENCRYPTION_KEY)
except ValueError:
    print("ADVERTENCIA: La clave de cifrado no es válida. Usando clave de respaldo para desarrollo.")
    # Clave de respaldo si la clave principal es incorrecta
    cipher_suite = Fernet(b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=') 

def encrypt_embedding(embedding_bytes: bytes) -> bytes:
    """Cifra el vector embedding usando Fernet (AES)."""
    return cipher_suite.encrypt(embedding_bytes)

def decrypt_embedding(encrypted_bytes: bytes) -> bytes:
    """Descifra el vector embedding."""
    return cipher_suite.decrypt(encrypted_bytes)