import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from api.utils.cluster import guardar_modelo, cargar_modelo

# Archivos de modelo (se asume que se guardan en el mismo directorio que el script)
MODELO_FILE = "modelo_kmeans.joblib"
SCALER_FILE = "scaler.joblib"
METADATA_FILE = "metadata_kmeans.joblib" 


class KMeansService:
    def __init__(self, df: pd.DataFrame):
        # El DataFrame inicial aquí es meramente un placeholder para el init
        self.df = df.copy() 
        self.model = None
        self.scaler = None
        self.features = None

    def entrenar_modelo(self, features=None, n_clusters=3, raw_data_list=None):
        if raw_data_list is None or not raw_data_list:
             raise ValueError("No se proporcionaron datos para el entrenamiento.")
        
        # 1. Crear el DataFrame a partir de los datos recibidos (lista de dicts del JSON)
        self.df = pd.DataFrame(raw_data_list) 

        # 2. Determinar Features
        if features is None:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist() 
            if len(numeric_cols) < 2:
                raise ValueError("Se necesitan al menos dos columnas numéricas.")
            features = numeric_cols[:2]
        
        self.features = features
        X = self.df[features].dropna() 
        
        if len(X) < 5:
            raise ValueError("Se requieren al menos 5 filas de datos válidos para el entrenamiento.")


        # 3. Escalamiento
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        # 4. Modelo K-Means
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        etiquetas = self.model.fit_predict(X_scaled)
        self.df.loc[X.index, "cluster"] = etiquetas

        # 5. Guardar modelo, scaler Y metadata (features)
        guardar_modelo(self.model, MODELO_FILE)
        guardar_modelo(self.scaler, SCALER_FILE)
        guardar_modelo({"features": self.features}, METADATA_FILE) 

        # 6. Resultados
        centroides = self.scaler.inverse_transform(self.model.cluster_centers_).tolist()
        conteo = dict(pd.Series(etiquetas).value_counts().sort_index().to_dict())

        return {
            "características": features,
            "n_clusters": n_clusters,
            "centroides": centroides,
            "distribución_clusters": conteo,
            "filas_entrenadas": len(X),
            "muestra_etiquetada": self.df.loc[X.index, features + ["cluster"]].head(10).to_dict(orient="records")
        }

    def predecir_cluster(self, muestras):
        # 1. Cargar modelo, scaler Y metadata
        modelo = cargar_modelo(MODELO_FILE)
        scaler = cargar_modelo(SCALER_FILE)
        metadata = cargar_modelo(METADATA_FILE) 
        
        # 2. Crear DataFrame de muestras y asegurar el orden de las columnas
        features = metadata["features"]
        # Asume que 'muestras' es una lista de dicts con claves = features
        df_muestras = pd.DataFrame(muestras, columns=features) 
        
        # 3. Transformar y predecir
        muestras_escaladas = scaler.transform(df_muestras)
        predicciones = modelo.predict(muestras_escaladas)

        return {"predicciones": predicciones.tolist()}