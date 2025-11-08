import joblib
import os

# Guardar modelo o scaler
def guardar_modelo(objeto, nombre_archivo):
    try:
        joblib.dump(objeto, nombre_archivo)
    except Exception as e:
        raise Exception(f"No se pudo guardar el modelo: {e}")

# Cargar modelo o scaler
def cargar_modelo(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        raise FileNotFoundError(f"No se encontró el archivo: {nombre_archivo}")
    return joblib.load(nombre_archivo)
