from api.utils.regresion_simple import calcular_regresion_lineal_simple

def ejecutar_analisis_rls(data_points, nombres_variables):
    """
    Coordina la preparación de datos, realiza validaciones y ejecuta el cálculo de RLS.
    
    Args:
        data_points (list): Lista de diccionarios DataPoint (contiene 'x' y 'y').
        nombres_variables (list): Nombres de la variable predictora X (debe ser una lista con 1 elemento).

    Returns:
        dict: Resultados del modelo y datos de entrada.
    """
    
    # 1. Validaciones básicas RLS
    if not data_points or len(data_points) < 3:
        raise ValueError("Se requieren al menos 3 puntos de datos para el análisis.")
    
    # RESTRICCIÓN CLAVE RLS: Debe haber exactamente 1 variable X
    if len(nombres_variables) != 1:
        raise ValueError("La Regresión Lineal Simple requiere seleccionar exactamente una variable predictora (X).")
        
    nombre_variable_x = nombres_variables[0]

    # 2. Separar X (predictora) e Y (objetivo)
    X_raw = [point["x"] for point in data_points] # Esto será [[x1], [x2], ...]
    Y_raw = [point["y"] for point in data_points]
    
    # 3. Validar la consistencia de las dimensiones (solo 1 variable por fila)
    num_vars = 1
    for x_row in X_raw:
        if len(x_row) != num_vars:
            raise ValueError(
                f"Inconsistencia de datos. Se espera 1 variable por fila para RLS, pero se encontró una fila con {len(x_row)}."
            )

    # 4. Calcular el modelo de regresión simple
    resultados_calculados = calcular_regresion_lineal_simple(
        X_raw, 
        Y_raw, 
        nombre_variable_x
    )

    # 5. Devolver la estructura completa
    return {
        **resultados_calculados,
        "datos_entrada": data_points,
        "nombres_variables": nombres_variables, # Se mantiene como lista para la vista
    }