"""
Import Necessary Libraries 
"""
from flask import Flask, request
from flask_caching import Cache
import csv

"""
Flask App Initiation and Flask Cache Setup
"""
cache = Cache()
app = Flask(__name__)
app.config["CACHE_TYPE"] = "simple"
cache.init_app(app)

"""
Functions used in Flask App
"""
@cache.cached(timeout=3600, key_prefix="thetas")
def read_coefficient(filename):
    """this function takes the csv file as input,
        reads the file, returns the list of
        coefficients, and caches the data for
        later use

    Args:
        filename (string): name of file to be read

    Returns:
        [List]: the coefficients read from the file
    """
    with open(filename, "r") as f:
        data = csv.reader(f)
        coefficients = []
        for line in data:
            coefficients.append([float(x) for x in line])
        return coefficients

def get_data():
    """Extracts the data from the post request

    Returns:
        [List]: List of feature values
    """
    data = []
    data.append(request.args.get("date"))
    data.append(request.args.get("house_age"))
    data.append(request.args.get("station_distance"))
    data.append(request.args.get("stores"))
    data.append(request.args.get("latitude"))
    data.append(request.args.get("longitude"))

    return data


def predicted_price(theta0, thetas, data):
    """using the hypothesis linear eqation to
        compute the estamited price bulit by
        the Linear Model

    Args:
        theta0 (float): the intercept of the linear equation
        thetas (float): the coefficients of the linear equation (theta1----theta6)
        data (List): the parameters of the linear equation (x1----x6)

    Returns:
        [Float]: the output of the linear equation (estimated price)
    """

    price = 0
    for index, feature in enumerate(data):
        price += float(feature) * float(thetas[index])

    price += theta0

    return price


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
        coefficients = read_coefficient("lm_parameters.csv")
        data = get_data()
        thetas = coefficients[0]
        theta0 = coefficients[1][0]
        return (
            "The house is evaluated at: "
            + str(predicted_price(theta0, thetas, data))
            + " per unit area"
        )


"""
Flask App Entry Point (Main)
"""
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
