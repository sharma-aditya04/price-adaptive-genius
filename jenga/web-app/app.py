from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# Load the trained model
with open('model/trained_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/', methods=['GET', 'POST'])
def index():
    ai_price = None
    if request.method == 'POST':
        amazon_url = request.form.get('amazon_url')
        flipkart_url = request.form.get('flipkart_url', 0)

        # Process the URLs and make a prediction
        ai_price = predict_price(amazon_url, flipkart_url)

    return render_template('index.html', ai_price=ai_price)

def predict_price(amazon_url, flipkart_url):
    # Here you would implement the logic to process the URLs and use the model to predict the price
    # This is a placeholder for the actual prediction logic
    # For example, you might extract features from the URLs and pass them to the model
    features = extract_features(amazon_url, flipkart_url)
    return model.predict([features])[0]

def extract_features(amazon_url, flipkart_url):
    # Placeholder for feature extraction logic
    # This function should convert the URLs into a format suitable for the model
    return [0]  # Replace with actual feature extraction

if __name__ == '__main__':
    app.run(debug=True)