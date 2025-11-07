import numpy as np

def calcular_regresion_lineal_multiple(X_raw, Y_raw, nombres_variables):
    """
    Calcula el modelo de Regresión Lineal Múltiple (OLS).

    Args:
        X_raw (list of list of float): Variables predictoras.
        Y_raw (list of float): Variable objetivo.
        nombres_variables (list of str): Nombres de las variables X.

    Returns:
        dict: Diccionario con los resultados del modelo (coeficientes, R2, ecuación, etc.)
    """
    
    # 1. Preparación de los datos: Convertir a arrays de NumPy
    # Y debe ser una columna (vector)
    Y = np.array(Y_raw).reshape(-1, 1) 
    
    # X debe incluir una columna de unos para el intercepto (B0)
    X_data = np.array(X_raw)
    n_observaciones = X_data.shape[0]
    
    # Añadir columna de unos (intercepto) al inicio de X
    X = np.insert(X_data, 0, 1, axis=1) 

    # 2. CÁLCULO DE COEFICIENTES (B = (X^T * X)^-1 * X^T * Y)
    try:
        # X transpuesta
        XT = X.T
        
        # (X^T * X)
        XTX = XT @ X
        
        # (X^T * X)^-1
        XTX_inv = np.linalg.inv(XTX)
        
        # B = (X^T * X)^-1 * X^T * Y
        B = XTX_inv @ XT @ Y
        
        # Coeficientes: B0, B1, B2, ...
        coeficientes = B.flatten().tolist()
    
    except np.linalg.LinAlgError:
        # Esto ocurre si la matriz XTX es singular (ej. multicolinealidad perfecta o pocos datos)
        raise ValueError("Error de cálculo: La matriz de entrada no es invertible. Verifica si tienes variables linealmente dependientes o muy pocos datos.")
        
    # 3. PREDICCIONES Y RESIDUOS
    Y_pred = X @ B  # Y_estimado = X * B
    residuos = Y - Y_pred
    
    # 4. CÁLCULO DE R-CUADRADO (R²)
    # Varianza total (SST - Suma de Cuadrados Total)
    SST = np.sum((Y - np.mean(Y))**2)
    
    # Varianza residual (SSE - Suma de Cuadrados del Error)
    SSE = np.sum(residuos**2)
    
    # Coeficiente de Determinación R² = 1 - (SSE / SST)
    r2 = 1 - (SSE / SST)
    
    # 5. CONSTRUCCIÓN DE LA ECUACIÓN
    ecuacion = f"Y = {coeficientes[0]:.4f}" # Intercepto
    for i in range(len(nombres_variables)):
        signo = " + " if coeficientes[i + 1] >= 0 else " - "
        ecuacion += f"{signo}{abs(coeficientes[i + 1]):.4f} * {nombres_variables[i]}"

    return {
        "coeficientes": [float(c) for c in coeficientes],
        "r2": float(r2),
        "ecuacion": ecuacion,
        "predicciones": [float(y) for y in Y_pred.flatten()],
        "residuos": [float(r) for r in residuos.flatten()],
    }