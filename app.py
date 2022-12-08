from flask import Flask, request, render_template,Response
from flask_cors import CORS
import utilities
from werkzeug.utils import secure_filename
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
        user_name=Members[person]
        print(Members[person])
        print(predict("Voc"))
    else:
        print("Unknown")
        user_name="Unknown"
    print(Prediction)
    return [user_name]

@app.route('/check-statement', methods=['POST'])
def check_statement():
    return

@app.route("/plot-data",methods=['POST'])
def plot_data():
    x,y,z,scatter_x,scatter_y = utilities.dataToDraw()

    return[x,y,z,scatter_x,scatter_y]


if __name__ == "__main__":
    app.run(debug=True, port=5001)
