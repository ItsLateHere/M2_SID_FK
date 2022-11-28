# Endpoints of the app
from flask import Flask, request, jsonify, Blueprint

api_controller = Blueprint('api_controller', __name__)

tweets = [
    {"id": 1, "text": "fbef huifhez ihgze fih fzefajzfnhozef noijfe fo", "class": 1},
]

@api_controller.route("/api/faketest" , methods=['GET'])
def is_fake():
    return jsonify(tweets)