# app.py
from flask import Flask, request, jsonify
from data import formatted_data
from date_util import parser

app = Flask(__name__)

app.config.update(
    FLASK_ENV='development'
)

app.debug=True

@app.route("/open-restaurants", methods=['GET'])
def get_open_restaurants():
    print(request.args.get('date'))
    return jsonify(formatted_data)

# @app.post("/countries")
# def add_country():
#     if request.is_json:
#         country = request.get_json()
#         country["id"] = _find_next_id()
#         countries.append(country)
#         return country, 201
#     return {"error": "Request must be JSON"}, 415