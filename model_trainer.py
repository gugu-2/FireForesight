import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
import joblib
import logging

logging.basicConfig(level=logging.INFO)

def train_model(data):
    try:
        features = ['lat', 'lon', 'temp', 'humidity', 'wind_speed', 'ndvi', 'fire_history']
        X = data[features]
        y = data['fire_occurred']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        rf = RandomForestClassifier(random_state=42)
        param_grid = {'n_estimators': [100, 200], 'max_depth': [10, 20, None]}
        grid_search = GridSearchCV(rf, param_grid, cv=5)
        grid_search.fit(X_train, y_train)
        joblib.dump(grid_search.best_estimator_, 'wildfire_model.pkl')
        logging.info("Model trained and saved")
    except Exception as e:
        logging.error(f"Error training model: {e}")
        raise