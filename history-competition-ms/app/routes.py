from flask import Blueprint, jsonify
from app.services import get_historical_winners

competition_routes = Blueprint('competition_routes', __name__)

# Ruta para obtener los ganadores históricos de todas las competencias
@competition_routes.route('/compe/history', methods=['GET'])
def get_historical_winners_endpoint():
    winners = get_historical_winners()

    if winners:
        return jsonify({
            "status": "success",
            "historical_winners": winners
        })
    else:
        return jsonify({
            "status": "no-data",
            "message": "No se encontraron ganadores históricos."
        }), 404
