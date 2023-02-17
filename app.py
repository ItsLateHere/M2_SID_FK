from flask import Flask, render_template
from flask import Flask,request
from api.api_controller import api_controller
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.register_blueprint(api_controller)

@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", ssl_context=('data/certificates/fullchain1.pem','privkey1.pem'))
