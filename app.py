from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
with open('D:\My Data\Desktop\project\RF.pkl', 'rb') as f:  
    RF = pickle.load(f)

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/aqi_pred', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
        try:
            # Retrieve form inputs
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

            # Create input array for the model
            user_input = np.array([[pm25, pm10, no, no2, nox, co, so2, o3, benzene, toluene, xylene, year, month, day]])

            # Make predictions
            prediction = RF.predict(user_input)[0]

            # Determine air quality category
            if 0 <= prediction <= 50:
                category = "Good"
                health_impact = "Air quality is satisfactory, and air pollution poses little or no risk."
            elif 51 <= prediction <= 100:
                category = "Moderate"
                health_impact = "Air quality is acceptable. There may be a risk for some people."
            elif 101 <= prediction <= 150:
                category = "Unhealthy for Sensitive Groups"
                health_impact = "Members of sensitive groups may experience health effects."
            elif 151 <= prediction <= 200:
                category = "Unhealthy"
                health_impact = "Some members of the general public may experience health effects."
            elif 201 <= prediction <= 300:
                category = "Very Unhealthy"
                health_impact = "Health alert: The risk of health effects is increased for everyone."
            else:
                category = "Hazardous"
                health_impact = "Health warning of emergency conditions: everyone is more likely to be affected."

            result = f"Predicted AQI: {prediction:.2f} ({category})"
            description = health_impact

            # Return the prediction result and description
            return render_template('aqi_pred.html', predicted_aqi=result, description=description)

        except Exception as e:
            return f"An error occurred: {str(e)}"

    # For GET request, simply render the prediction form page
    return render_template("aqi_pred.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
