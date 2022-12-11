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
username= "Unknown"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict-user', methods=['POST'])
def predict_user():
    global username
    file = request.files['source']
    file.save("audio.wav")
    Prediction=predict("Voice")
    person= np.argmax(Prediction)
    print(Prediction)
    counter=0
    Members=["Dina","Romaisaa","Shaaban"]
    for i in range(3):
        threshold= 0.7
        if person==2:
            threshold=2
        if np.abs(Prediction[person]-Prediction[i])<threshold:
            counter+=1
    if counter==1:
        user_name=Members[person]
        print(Members[person])
    else:
        print("Unknown")
        user_name="Unknown"
    print(Prediction)
    username=user_name
    return [user_name]

@app.route("/plot-data",methods=['POST'])
def plot_data():
    global username
    x,y,z,scatter_x,scatter_y,x2,y2,z2,scatter_x2,scatter_y2 = utilities.dataToDraw(username)

    return[x,y,z,scatter_x,scatter_y,x2,y2,z2,scatter_x2,scatter_y2]


if __name__ == "__main__":
    app.run(debug=True, port=5001)
