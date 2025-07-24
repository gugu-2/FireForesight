from flask import Flask, jsonify
import joblib
import numpy as np
import logging

app = Flask(__name__)
model = joblib.load('wildfire_model.pkl')
logging.basicConfig(level=logging.INFO)

@app.route('/api/predict', methods=['GET'])
def predict():
    try:
        grid_points = [
            {'lat': 34.05, 'lon': -118.24, 'temp': 30.5, 'humidity': 20.0, 'wind_speed': 5.0, 'ndvi': 0.4, 'fire_history': 2},
            # Add more grid points
        ]
        predictions = []
        for point in grid_points:
            features = np.array([[point['lat'], point['lon'], point['temp'], point['humidity'], point['wind_speed'], point['ndvi'], point['fire_history']]])
            risk_prob = model.predict_proba(features)[:, 1][0]
            predictions.append({'lat': point['lat'], 'lon': point['lon'], 'risk_prob': risk_prob})
        logging.info("Predictions generated")
        return jsonify(predictions)
    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)