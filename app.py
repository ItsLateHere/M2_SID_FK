from flask import Flask, render_template
from flask import Flask,request
from api.api_controller import api_controller
from flask_cors import CORS, cross_origin
from model.SVM import SVM


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.register_blueprint(api_controller)

@app.route('/')
def hello_world():  # put application's code here
    #return render_template('index.html')
    args = request.args
    input=args.get("input")
    print(input)
    svm=SVM()
    #svm.train()
    out=svm.predict(input)
    return input+' '+out


if __name__ == '__main__':
    app.run(host="0.0.0.0")
