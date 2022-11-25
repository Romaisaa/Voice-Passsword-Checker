from flask import Flask, request, render_template,Response
from flask_cors import CORS
import librosa
from werkzeug.utils import secure_filename
import os

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
    file = request.files['source']
    data,fs= librosa.load(file)
    # print(fs)
    return ["User Name"]

@app.route('/check-statement', methods=['POST'])
def check_statement():
    return






if __name__ == "__main__":
    app.run(debug=True, port=5001)
