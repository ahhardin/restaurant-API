# app.py

# third party
import arrow
from flask import Flask, request, jsonify
import json

# internal
from data import formatted_data, get_open_restaurants_by_date

app = Flask(__name__)


@app.route("/open-restaurants", methods=['GET'])
def get_open_restaurants():
    date_str = request.args.get('date')
    print('date str', date_str)
    try: date = arrow.get(request.args.get('date'))
    except: return jsonify({"error": "You must include a valid url-encoded date param"}), 400
    open_restaurants = []
    open_restaurants = get_open_restaurants_by_date(date)
    return jsonify(open_restaurants)

@app.route("/formatted-data", methods=['GET'])
def get_formatted_data():
    jsonObj = json.dumps(formatted_data, default=str)
    return json.loads(jsonObj)
