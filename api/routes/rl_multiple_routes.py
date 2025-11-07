from flask import Blueprint, request, jsonify
from api.services.rl_multiple_service import ejecutar_analisis_rlm

rl_multiple_bp = Blueprint("rl_multiple", __name__, url_prefix="/api")

@rl_multiple_bp.route("/rl-multiple/analizar", methods=["POST"])
def analizar_regresion_multiple():
    try:
        data = request.get_json()
        
        # Extraer datos del cuerpo de la solicitud
        data_points = data.get("data_points", [])
        nombres_variables = data.get("nombres_variables", [])
        
        # Llamar al servicio para procesar y calcular.
        resultados_finales = ejecutar_analisis_rlm(
            data_points, 
            nombres_variables
        )

        # Devolver el resultado
        return jsonify(resultados_finales)
        
    except ValueError as ve:
        # Captura errores específicos de cálculo o validación
        return jsonify({"error": str(ve)}), 400
        
    except Exception as e:
        print(f"Error interno en la API: {e}")
        return jsonify({"error": "Ocurrió un error interno del servidor al procesar la regresión."}), 500