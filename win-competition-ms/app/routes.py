from flask import Blueprint, jsonify
from app.services import get_winner

competition_routes = Blueprint('competition_routes', __name__)

# Ruta para obtener el o los ganadores de la competencia
@competition_routes.route('/compe/win/<competition_id>', methods=['GET'])
def get_winner_endpoint(competition_id):
    winners, error_message = get_winner(competition_id)

    if winners:
        return jsonify({
            "status": "finished",
            "winners": winners
        })
    else:
        return jsonify({
            "status": "in-progress",
            "message": error_message
        }), 400
