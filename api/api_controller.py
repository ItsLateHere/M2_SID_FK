# Endpoints of the app
from flask import Flask, request, jsonify, Blueprint
from model.SVM import SVM
from controllers.tweet_controller import *

api_controller = Blueprint('api_controller', __name__)

tweets = [
    {"id": 1, "text": "fbef huifhez ihgze fih fzefajzfnhozef noijfe fo", "class": 1},
]


@api_controller.route("/api/inputTest", methods=['POST'])
def input_is_fake():
    svm = SVM()
    request_data = request.get_json()

    result = svm.predict(svm.wordopt(request_data["tweet_text"]))
    if result[:13] == "is false with":
        request_data["is_fake"] = 1
        request_data["msg_res"] = result
    else:
        request_data["is_fake"] = 0
        request_data["msg_res"] = result

    return response_format(request_data, 0, 200)


@api_controller.route("/api/faketest", methods=['POST'])
def is_fake():
    try:
        co_fake = 0
        svm = SVM()
        request_data = request.get_json()

        print(request_data)
        for a in request_data:
            result = svm.predict(svm.wordopt(a["tweet_text"]))

            if result[:13] == "is false with":
                co_fake = co_fake + 1
                a["is_fake"] = 1
                a["msg_res"] = result
            else:
                a["is_fake"] = 0
                a["msg_res"] = result

        return response_format(request_data, co_fake, 200)
    finally:
        saveTweets(request_data)



def response_format(articles_list, nbr_fake, response_code):
    res = {
        "articles": articles_list,
        "number_fake": nbr_fake,
        "code": response_code
    }

    return jsonify(res)
