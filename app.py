# app.py

# third party
import arrow
from flask import Flask, request, jsonify

# internal
from data import formatted_data, ordered_day_abbreviations

app = Flask(__name__)

@app.route("/open-restaurants", methods=['GET'])
def get_open_restaurants():
    date = arrow.get(request.args.get('date'))
    open_restaurants = []
    weekday = ordered_day_abbreviations[date.weekday()]
    time = date.time()
    for key, val in formatted_data.items():
        time_intervals = val.get(weekday)
        if time_intervals:
            for time_interval in time_intervals:
                if time > time_interval[0] and time < time_interval[1]:
                    open_restaurants.append(key)
            
    return jsonify(open_restaurants)

@app.route("/formatted_data", methods=['GET'])
def get_formatted_data():
    return jsonify(formatted_data)
