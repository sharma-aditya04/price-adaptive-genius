# data_processor.py
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class DataProcessor:
    def __init__(self):
        self.scaler = MinMaxScaler()
    
    def clean_data(self, raw_df):
        df = raw_df.copy()
        # Handle missing values
        df['competitor_price'].fillna(df['competitor_price'].median(), inplace=True)
        df['demand'].interpolate(method='time', inplace=True)
        
        # Feature engineering
        df['price_difference'] = df['our_price'] - df['competitor_price']
        df['discount_pct'] = (df['base_price'] - df['our_price']) / df['base_price']
        
        return df
    
    def calculate_demand_score(self, df):
        window_size = '7D'
        df['demand_score'] = df['sales'].rolling(window_size).mean()
        return df
    
    def prepare_training_data(self, df):
        features = ['price', 'competitor_price', 'demand_score', 'day_of_week']
        scaled_features = self.scaler.fit_transform(df[features])
        return pd.DataFrame(scaled_features, columns=features)
