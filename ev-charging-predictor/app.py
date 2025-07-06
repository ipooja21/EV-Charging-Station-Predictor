from flask import Flask, render_template, request
from utils.data_loader import load_ev_stations_data
from utils.map_utils import create_map, cluster_ev_stations
from sklearn.linear_model import LinearRegression
import os

app = Flask(__name__)

CSV_FILE_PATH = os.path.join("C:\\Users\\RANGBAAZ\\Desktop\\ev-charging-prediction\\ev-charging-stations-india.csv")


@app.route('/')
def index():
    return render_template('index.html', map_path=None, predicted_stations=None)


def predict_ev_demand(pop_density):
    X = [[10000], [20000], [30000], [40000]]
    y = [10, 20, 35, 50]
    model = LinearRegression()
    model.fit(X, y)
    predicted_demand = model.predict([[pop_density]])
    return int(predicted_demand[0])


@app.route('/predict', methods=['POST'])
def predict():
    city_name = request.form.get('city_name')
    try:
        pop_density = int(request.form.get('pop_density', 20000))
    except ValueError:
        return "Invalid population density provided. Please enter a numeric value."

    ev_data = load_ev_stations_data(CSV_FILE_PATH)
    if ev_data is not None:
        city_stations = ev_data[ev_data['City'].str.lower() == city_name.lower()]
        locations = city_stations[['Latitude', 'Longitude']].values

        predicted_demand = predict_ev_demand(pop_density)
        station_count = max(1, predicted_demand // 10)

        if len(locations) > 0:
            predicted_stations = cluster_ev_stations(locations, station_count)
            map_path = create_map(locations, predicted_stations)
            return render_template(
                'index.html',
                map_path=map_path,
                predicted_stations=predicted_stations,
                station_count=len(predicted_stations)
            )
        else:
            return f"No EV station data available for {city_name}."
    else:
        return "Error loading EV station data."


if __name__ == '__main__':
    app.run(debug=True)
