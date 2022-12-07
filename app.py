from flask import Flask, request, render_template,Response
from flask_cors import CORS
import librosa
from werkzeug.utils import secure_filename
import os
from Gmm import predict
from Randomforrest import predict_voice
import numpy as np
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
    file.save("audio.wav")
    Prediction=predict("Voice")
    print(predict_voice())
    person= np.argmax(Prediction)
    counter=0
    Members=["Dina","Romasiaa","Shaaban"]
    for i in range(3):
        if np.abs(Prediction[person]-Prediction[i])<1:
            counter+=1
    if counter==1:
        print(Members[person])
        print(predict("Voc"))
    else:
        print("Unknown")
    print(Prediction)
    return ["Happend"]

@app.route('/check-statement', methods=['POST'])
def check_statement():
    return






if __name__ == "__main__":
    app.run(debug=True, port=5001)
