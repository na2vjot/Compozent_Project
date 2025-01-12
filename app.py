from flask import Flask, request, render_template
import pickle
import numpy as np
import xgboost as xgb

app = Flask(__name__)

# Load the trained XGBoost model from pickle
with open('D:\My Data\Desktop\project\model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the encoder for 'City' used during training
with open('D:\My Data\Desktop\project\encoder.pkl', 'rb') as enc_file:
    city_encoder = pickle.load(enc_file)

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == "POST":
        # Get the form data from the user input
        pm25 = float(request.form.get("PM2.5"))
        pm10 = float(request.form.get("PM10"))
        no = float(request.form.get("NO"))
        no2 = float(request.form.get("NO2"))
        nox = float(request.form.get("NOx"))
        co = float(request.form.get("CO"))
        so2 = float(request.form.get("SO2"))
        o3 = float(request.form.get("O3"))
        benzene = float(request.form.get("Benzene"))
        toluene = float(request.form.get("Toluene"))
        xylene = float(request.form.get("Xylene"))
        year = int(request.form.get("Year"))
        month = int(request.form.get("Month"))
        day = int(request.form.get("Day"))

        # Use a default or pre-determined encoded value for 'City' (you can adjust this value)
        # Here, we assume 'City' has been label-encoded and the default is '0' (adjust if needed)
        default_city_encoded = 0  # or any other default city index

        # Prepare the user input array, including the default encoded value for 'City'
        user_input = np.array([[default_city_encoded, pm25, pm10, no, no2, nox, co, so2, o3, benzene, toluene, xylene, year, month, day]])

        # Ensure the input data has the same shape and column order as the training data
        expected_columns = ['City', 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene', 'Year', 'Month', 'Day']
        
        if user_input.shape[1] != len(expected_columns):
            return "Error: Input data does not have the expected number of columns"

        # Convert the input data into a DMatrix
        dmatrix_input = xgb.DMatrix(user_input, feature_names=expected_columns)

        # Make the prediction using the trained model
        model_output = model.predict(dmatrix_input)

        # Process the prediction result (assuming regression output)
        output_user = f"Predicted AQI: {model_output[0]}"

        # Render the result on the index page
        return render_template('index.html', predicted_aqi=output_user)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
