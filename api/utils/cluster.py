import joblib
import os

# Guardar modelo o scaler
def guardar_modelo(objeto, nombre_archivo):
    try:
        # Asegúrate de que el directorio existe si estás guardando en una ruta específica
        # Por ahora, se guarda en la raíz o donde se ejecuta el script.
        joblib.dump(objeto, nombre_archivo)
    except Exception as e:
        # Usamos una excepción más genérica si no queremos propagar joblib.
        raise Exception(f"No se pudo guardar el modelo/scaler: {e}")

# Cargar modelo o scaler
def cargar_modelo(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        raise FileNotFoundError(f"No se encontró el archivo: {nombre_archivo}")
    return joblib.load(nombre_archivo)