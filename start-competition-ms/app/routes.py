from flask import Blueprint, jsonify
from app.services import start_competition

competition_routes = Blueprint('competition_routes', __name__)

@competition_routes.route('/compe/start', methods=['POST'])
def start_competition_endpoint():
    response = start_competition()
    return jsonify(response)
