from flask import Flask, request, render_template,Response
from flask_cors import CORS

app = Flask(__name__, template_folder='./template', static_folder='./static')
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        'origins': '*'
    }
})


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict-user', methods=['POST'])
def predict_user():
    user="romaisaa"
    # Response("{'a':'b'}", status=201, mimetype='application/json')
    return list(user)

@app.route('/check-statement', methods=['POST'])
def check_statement():
    return






if __name__ == "__main__":
    app.run(debug=True, port=5001)
