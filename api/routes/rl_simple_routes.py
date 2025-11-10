from flask import Blueprint, request, jsonify
from api.services.rl_simple_service import ejecutar_analisis_rls

rl_simple_bp = Blueprint("rl_simple", __name__, url_prefix="/api")

@rl_simple_bp.route("/rl-simple/analizar", methods=["POST"])
def analizar_regresion_simple():
    try:
        data = request.get_json()
        
        # Extraer datos del cuerpo de la solicitud
        data_points = data.get("data_points", [])
        nombres_variables = data.get("nombres_variables", []) # Espera una lista con 1 nombre
        
        # Llamar al servicio para procesar y calcular.
        # El servicio rl_simple_service ya valida que len(nombres_variables) == 1
        resultados_finales = ejecutar_analisis_rls(
            data_points, 
            nombres_variables
        )

        # Devolver el resultado
        return jsonify(resultados_finales)
        
    except ValueError as ve:
        # Captura errores específicos de cálculo o validación (ej. RLS requiere 1 variable)
        return jsonify({"error": str(ve)}), 400
        
    except Exception as e:
        print(f"Error interno en la API: {e}")
        return jsonify({"error": "Ocurrió un error interno del servidor al procesar la regresión simple."}), 500