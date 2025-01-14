from flask import Flask, request, render_template
import pickle
import numpy as np
import xgboost as xgb

app = Flask(__name__)

# Load the trained XGBoost model from pickle
with open('D:\My Data\Desktop\project\RF.pkl', 'rb') as f:
    RF = pickle.load(f)

# # Load the encoder for 'City' used during training
# with open('D:\My Data\Desktop\project\encoder.pkl', 'rb') as enc_file:
#     city_encoder = pickle.load(enc_file)

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == "POST":
        try:
            # Retrieve form inputs with default values
            pm25 = request.form.get("PM2.5", type=float, default=0.0)
            pm10 = request.form.get("PM10", type=float, default=0.0)
            no = request.form.get("NO", type=float, default=0.0)
            no2 = request.form.get("NO2", type=float, default=0.0)
            nox = request.form.get("NOx", type=float, default=0.0)
            co = request.form.get("CO", type=float, default=0.0)
            so2 = request.form.get("SO2", type=float, default=0.0)
            o3 = request.form.get("O3", type=float, default=0.0)
            benzene = request.form.get("Benzene", type=float, default=0.0)
            toluene = request.form.get("Toluene", type=float, default=0.0)
            xylene = request.form.get("Xylene", type=float, default=0.0)
            year = request.form.get("Year", type=int, default=2020)
            month = request.form.get("Month", type=int, default=1)
            day = request.form.get("Day", type=int, default=1)

            # Set a default encoded value for 'City'
            # default_city_encoded = 0  # Assuming 0 corresponds to Mumbai

            # Create input array for the model
            user_input = np.array([[pm25, pm10, no, no2, nox, co, so2, o3, benzene, toluene, xylene, year, month, day]])

            # Make predictions
            prediction = RF.predict(user_input)

            # Format the output
            result = f"Predicted AQI: {prediction[0]:.2f}"

            return render_template('index.html', predicted_aqi=result)

        except Exception as e:
            # Handle exceptions gracefully
            return f"An error occurred: {str(e)}"



if __name__ == "__main__":
    app.run(debug=True, port=8000)

