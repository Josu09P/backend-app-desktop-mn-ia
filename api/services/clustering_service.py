import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from api.utils.cluster import guardar_modelo, cargar_modelo

class KMeansService:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.model = None
        self.scaler = None
        self.features = None

    def entrenar_modelo(self, features=None, n_clusters=3):
        # Si no se especifican columnas, se usan las dos primeras numéricas
        if features is None:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns.to|list()
            if len(numeric_cols) < 2:
                raise ValueError("Se necesitan al menos dos columnas numéricas.")
            features = numeric_cols[:2]
        
        self.features = features
        X = self.df[features].dropna()

        # Escalamiento
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        # Modelo K-Means
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        etiquetas = self.model.fit_predict(X_scaled)
        self.df.loc[X.index, "cluster"] = etiquetas

        # Guardar modelo y scaler
        guardar_modelo(self.model, "modelo_kmeans.joblib")
        guardar_modelo(self.scaler, "scaler.joblib")

        # Resultados
        centroides = self.scaler.inverse_transform(self.model.cluster_centers_).tolist()
        conteo = dict(pd.Series(etiquetas).value_counts().sort_index().to_dict())

        return {
            "características": features,
            "n_clusters": n_clusters,
            "centroides": centroides,
            "distribución_clusters": conteo,
            "muestra": self.df.head(10).to_dict(orient="records")
        }

    def predecir_cluster(self, muestras):
        modelo = cargar_modelo("modelo_kmeans.joblib")
        scaler = cargar_modelo("scaler.joblib")

        muestras_escaladas = scaler.transform(muestras)
        predicciones = modelo.predict(muestras_escaladas)

        return {"predicciones": predicciones.tolist()}
