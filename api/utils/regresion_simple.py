import numpy as np

def calcular_regresion_lineal_simple(X_raw, Y_raw, nombre_variable_x):
    """
    Calcula el modelo de Regresión Lineal Simple (OLS): Y = B0 + B1*X.

    Args:
        X_raw (list of list of float): Variable predictora ÚNICA (ej. [[x1], [x2], ...]).
        Y_raw (list of float): Variable objetivo.
        nombre_variable_x (str): Nombre de la única variable X.

    Returns:
        dict: Diccionario con los resultados del modelo (coeficientes, R2, ecuación, etc.)
    """

    # 1. Preparación de los datos: Convertir a arrays de NumPy
    # Y debe ser un vector columna
    Y = np.array(Y_raw).reshape(-1, 1)

    # X_data ahora es la única columna de la variable predictora, con forma N x 1
    # .flatten() y .reshape(-1, 1) aseguran la forma correcta si X_raw era [[x1], [x2], ...]
    X_data = np.array(X_raw).flatten().reshape(-1, 1)

    # Añadir columna de unos (intercepto B0) al inicio de X. X final es N x 2.
    n_observaciones = X_data.shape[0]
    X = np.insert(X_data, 0, 1, axis=1)

    # 2. CÁLCULO DE COEFICIENTES (B = (X^T * X)^-1 * X^T * Y)
    try:
        # Fórmulas de OLS para la matriz N x 2
        XT = X.T
        XTX = XT @ X
        XTX_inv = np.linalg.inv(XTX)
        B = XTX_inv @ XT @ Y

        # Coeficientes: B0 (Intercepto), B1 (Pendiente)
        coeficientes = B.flatten().tolist()

    except np.linalg.LinAlgError:
        # Error si la matriz es singular (ej. muy pocos datos, o todos los valores de X son iguales)
        raise ValueError("Error de cálculo: La matriz de entrada no es invertible. Verifica si tienes datos suficientes o si la variable X tiene varianza.")

    # 3. PREDICCIONES Y RESIDUOS
    Y_pred = X @ B  # Y_estimado = X * B
    residuos = Y - Y_pred

    # 4. CÁLCULO DE R-CUADRADO (R²)
    SST = np.sum((Y - np.mean(Y))**2)
    SSE = np.sum(residuos**2)
    r2 = 1 - (SSE / SST)

    # 5. CONSTRUCCIÓN DE LA ECUACIÓN (Y = B0 + B1*X)
    b0 = coeficientes[0]
    b1 = coeficientes[1]

    ecuacion = f"Y = {b0:.4f}" # Intercepto
    signo = " + " if b1 >= 0 else " - "
    ecuacion += f"{signo}{abs(b1):.4f} * {nombre_variable_x}"

    return {
        "coeficientes": [float(c) for c in coeficientes],
        "r2": float(r2),
        "ecuacion": ecuacion,
        "predicciones": [float(y) for y in Y_pred.flatten()],
        "residuos": [float(r) for r in residuos.flatten()],
    }