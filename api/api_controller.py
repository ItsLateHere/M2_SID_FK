# Endpoints of the app
from flask import Flask, request, jsonify, Blueprint
from model.SVM import SVM

api_controller = Blueprint('api_controller', __name__)

tweets = [
    {"id": 1, "text": "fbef huifhez ihgze fih fzefajzfnhozef noijfe fo", "class": 1},
]

@api_controller.route("/api/faketest" , methods=['POST'])
def is_fake():
    co_fake = 0
    svm =SVM()
    request_data = request.get_json()

    for a in request_data:
        result = svm.predict(svm.wordopt(a["tweet_text"]))

        if(result[:13] == "is false with"):
            co_fake = co_fake+1
            a["is_fake"] = 1
            a["msg_res"] = result
        else:
            a["is_fake"] = 0
            a["msg_res"] = result

    return response_format(request_data , co_fake , 200)

def response_format(articles_list , nbr_fake , response_code):
    res = {
        "articles" : articles_list,
        "number_fake" : nbr_fake,
        "code" : response_code
    }

    return jsonify(res)