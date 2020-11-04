#!/home/aobeid/anaconda3/bin/python
"""
Import Necessary Libraries 
"""
from flask import Flask, request
import pickle
import numpy as np
import argparse


app = Flask(__name__)

"""
Functions used in Flask App
"""
def read_arguments():
    """
    [summary]
    
    reading arguments from console


    Returns:
        [String]: path to model
    """
    parser = argparse.ArgumentParser(prog='Linear Regression Model',usage='%(prog)s [options] path to model')
    parser.add_argument('-path', type=str, help='Model Path',required=True)
    model_path = parser.parse_args()
    return model_path

def get_data():
    """Extracts the data from the post request

    Returns:
        [List]: List of feature values
    """
    data = []
    data.append(float(request.args.get("date")))
    data.append(float(request.args.get("house_age")))
    data.append(float(request.args.get("station_distance")))
    data.append(float(request.args.get("stores")))
    data.append(float(request.args.get("latitude")))
    data.append(float(request.args.get("longitude")))
    
    return np.array(data).reshape(1,6)

def predicted_price(data):
    """using the loaded linear model object to
        compute the estamited price.

    Args:
        data (List): the parameters of the linear equation (x1----x6)

    Returns:
        [Float]: the output of the linear Model Object
    """

    price = loaded_model.predict(data)

    return price[0]


"""
Flask App Routes
"""
@app.route("/")
def welcome():
    return "Welcome to my Model!"

@app.route("/predict", methods=["GET", "POST"])
def get_predicted_price():
    """Post Method to get the data from the request,
        compute the linear eqation, and return the
        estimated price as a respone


    Returns:
        [string]: Evaluation statment
    """

    if request.method == "POST":
        return (str(predicted_price(get_data())))

"""
Flask App Entry Point (Main)
"""
if __name__ == "__main__":
    #read arguments at app launch
    args = read_arguments()
    #load model at app launch
    loaded_model = pickle.load(open(args.path, 'rb'))
    app.run(debug=True, use_reloader=False,host='0.0.0.0')
