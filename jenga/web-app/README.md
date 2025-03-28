# Web App for AI Price Prediction

This project is a Flask web application that utilizes a trained machine learning model to predict prices based on Amazon and Flipkart URLs. The application allows users to input these URLs and receive an AI-generated price as output.

## Project Structure

```
web-app
├── app.py                # Main application file
├── model
│   └── trained_model.pkl # Serialized trained model
├── templates
│   └── index.html       # HTML template for user interface
├── static
│   ├── css
│   │   └── styles.css    # CSS styles for the web application
│   └── js
│       └── scripts.js     # JavaScript for client-side functionality
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd web-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   python app.py
   ```

5. **Access the web application:**
   Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- Input the Amazon URL and, optionally, the Flipkart URL in the provided fields.
- Click the "Submit" button to get the AI Price prediction.
- The result will be displayed on the same page.

## License

This project is licensed under the MIT License. See the LICENSE file for details.