from flask import Flask, request, jsonify
import joblib
import numpy as np

# Create Flask app
app = Flask(__name__)

# Load the trained XGBoost model
xgb_model = joblib.load("xgboost_model.joblib")  # Ensure the path to your model is correct

try:
    xgb_model = joblib.load("xgboost_model.joblib")
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")


# Define a route to make predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the data from the request
        data = request.get_json(force=True)

        # Extract the features from the incoming JSON data (ensure the data is in the expected format)
        features = np.array(data['features']).reshape(1, -1)

        # Make prediction using the loaded model
        prediction = xgb_model.predict(features)

        # Return the prediction as a JSON response
        return jsonify({'prediction': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Define the main function to run the app
if __name__ == '__main__':
    app.run(debug=True)
