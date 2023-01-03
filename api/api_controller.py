# Endpoints of the app
from flask import Flask, request, jsonify, Blueprint
from model.SVM import SVM

api_controller = Blueprint('api_controller', __name__)

tweets = [
    {"id": 1, "text": "fbef huifhez ihgze fih fzefajzfnhozef noijfe fo", "class": 1},
]

@api_controller.route("/api/faketest" , methods=['POST'])
def is_fake():
    svm =SVM()
    request_data = request.get_json()
    print(request_data)
    result = svm.predict(svm.wordopt(request_data["tweet"]))
    # print(result)

    return response_format(tweets , 2 , 200)

def response_format(articles_list , nbr_fake , response_code):
    res = {
        "artciles" : articles_list,
        "number_fake" : nbr_fake,
        "code" : response_code
    }

    return jsonify(res)