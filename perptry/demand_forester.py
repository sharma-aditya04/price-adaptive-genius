# demand_forecaster.py
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

class DemandForecaster:
    def build_lstm_model(self, input_shape):
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=input_shape),
            LSTM(50),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

# price_optimizer.py
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

class PriceOptimizer:
    def train_price_model(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        model = XGBRegressor(
            objective='reg:squarederror',
            n_estimators=1000,
            learning_rate=0.05
        )
        model.fit(X_train, y_train, eval_set=[(X_test, y_test)], early_stopping_rounds=50)
        return model
