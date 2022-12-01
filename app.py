from flask import Flask, render_template
from api.api_controller import api_controller


app = Flask(__name__)
app.register_blueprint(api_controller)

@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
