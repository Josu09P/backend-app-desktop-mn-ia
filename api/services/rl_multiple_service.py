from api.utils.regresion_multiple import calcular_regresion_lineal_multiple

def ejecutar_analisis_rlm(data_points, nombres_variables):
    """
    Coordina la preparación de datos, realiza validaciones y ejecuta el cálculo de RLM.
    
    Args:
        data_points (list): Lista de diccionarios DataPoint (contiene 'x' y 'y').
        nombres_variables (list): Nombres de las variables predictoras X.

    Returns:
        dict: Resultados del modelo y datos de entrada.
    """
    
    # 1. Validaciones básicas
    if not data_points or len(data_points) < 3:
        raise ValueError("Se requieren al menos 3 puntos de datos para el análisis.")
    
    if not nombres_variables:
        raise ValueError("Se requieren nombres de variables predictoras (X).")

    # 2. Separar X (predictoras) e Y (objetivo)
    X_raw = [point["x"] for point in data_points]
    Y_raw = [point["y"] for point in data_points]
    
    # 3. Validar la consistencia de las dimensiones
    num_vars = len(nombres_variables)
    for x_row in X_raw:
        if len(x_row) != num_vars:
            raise ValueError(
                f"Inconsistencia de datos. Se esperan {num_vars} variables por fila, pero se encontró una fila con {len(x_row)}."
            )

    # 4. Calcular el modelo de regresión
    resultados_calculados = calcular_regresion_lineal_multiple(
        X_raw, 
        Y_raw, 
        nombres_variables
    )

    # 5. Devolver la estructura completa
    return {
        **resultados_calculados,
        "datos_entrada": data_points,
        "nombres_variables": nombres_variables,
    }