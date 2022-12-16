from flask import Flask, request, render_template,Response
from flask_cors import CORS
import utilities
from Gmm import predict
import numpy as np
app = Flask(__name__, template_folder='./template', static_folder='./static')
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        'origins': '*'
    }
})
username= "Unknown"
prediction=[]
words=[]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict-user', methods=['POST'])
def predict_user():
    global prediction
    global words
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
            threshold=1.5
        if np.abs(Prediction[person]-Prediction[i])<threshold:
            counter+=1
    if counter==1:
        user_name=Members[person]
        words=predict("Voc",Members[person])
        wordIndex=np.argmax(words)
        if wordIndex!=1:
            user_name="Unknown"
    else:
        user_name="Unknown"
        words=[-27,-27,-27,-27]
    if max(Prediction)<=-30:
        user_name="ERROR"
    prediction=Prediction
    return [user_name]

@app.route("/plot-data",methods=['POST'])
def plot_data():
    global prediction
    global words
    prediction=np.array(prediction)+35
    predict=prediction.tolist()
    words=np.array(words)+27
    Words=words.tolist()
    print(Words)
    labels, mfcc,mfcc_coef,time, freq,amp = utilities.dataToDraw()

    return[ labels, mfcc,mfcc_coef,time, freq,amp ,predict, Words]


if __name__ == "__main__":
    app.run(debug=True, port=5001)

