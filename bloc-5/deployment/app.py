import numpy as np
import joblib

from flask import Flask, request, json, jsonify, render_template, flash, send_file
from werkzeug.exceptions import HTTPException

MODEL_PATH = "models/model.joblib"
app = Flask(__name__)
app.secret_key = "secretkey"

class MissingKeyError(HTTPException):
    # we can define our own error for the missing key
    code = 422
    name = "Missing key error"
    description = "JSON content missing key 'input'."

class MissingJSON(HTTPException):
    # we can define our own error for missing JSON
    code = 400
    name = "Missing JSON"
    description = "Missing JSON."

def make_prediction(physicochemical):
    """Return a prediction with our random forest classifier.
    """
    # load model
    classifier = joblib.load(MODEL_PATH)
    # make the prediction and return it
    # physicochemical = np.array(physicochemical)
    prediction = classifier.predict(physicochemical)
    return prediction

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors.
    """
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description
    })
    response.content_type = "application/json"
    return response

@app.route("/")
def index():
    flash("Wine Quality: ?")
    return render_template("index.html")

@app.route("/downloadsimple")
def download_simple_input():
    path = "simple_input.py"
    return send_file(path, as_attachment=True)

@app.route("/downloadmultiple")
def download_multiple_input():
    path = "multiple_input.py"
    return send_file(path, as_attachment=True)

@app.route("/predictAI", methods=["POST", "GET"])
def predictAI():
    input = request.form["list_float"].split(", ")
    for index, item in enumerate(input):
        input[index] = float(item)
    input = [input]
    
    prediction = make_prediction(input)
    flash("Wine Quality: " + str(prediction[0]))
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # check parameters
    if request.json:
        # get JSON as dictionnary
        json_input = request.get_json()
        if "input" not in json_input:
            # if "input" is not in our JSON we raise our own error
            raise MissingKeyError()
        
        # call our predict function that handle loading model and making a prediction
        prediction = make_prediction(json_input["input"])
        response = {
            "quality": prediction.tolist()
        }
        return jsonify(response), 200
    raise MissingJSON()

if __name__ == "__main__":
    app.run(debug=True)