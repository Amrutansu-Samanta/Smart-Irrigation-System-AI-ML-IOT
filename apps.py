from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
import pickle
import json
import subprocess
import sys
import os
import signal

app = Flask(__name__)

# Load model and scaler
model = tf.keras.models.load_model('mlp_model.keras')
with open('mlp_scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input from form
        soil_moisture = float(request.form['soil_moisture'])
        air_temp = float(request.form['air_temp'])
        air_humidity = float(request.form['air_humidity'])

        # Scale input
        features = np.array([[soil_moisture, air_temp, air_humidity]])
        features_scaled = scaler.transform(features)

        # Predict
        prediction = model.predict(features_scaled)[0][0]
        status = 'ON' if prediction > 0.5 else 'OFF'

        return render_template('index.html',
                               prediction_text=f'Pump Status Prediction: {status} (Confidence: {prediction:.2f})')
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")

@app.route('/sensor_data')
def sensor_data():
    try:
        with open("sensor_data.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

def handle_sigint(sig, frame):
    print("\nServer stopped by user (KeyboardInterrupt).")
    if os.path.exists("sensor_data.json"):
        os.remove("sensor_data.json")
    sys.exit(0)

if __name__ == '__main__':
    # Only set signal handler in the child process, not the reloader or parent. To handle keyboard interrupts gracefully
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        signal.signal(signal.SIGINT, handle_sigint)
    try:
        # Start ArduinoSerial.py as a background process if not already running
        import psutil
        script_running = False
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['cmdline'] and 'ArduinoSerial.py' in ' '.join(proc.info['cmdline']):
                script_running = True
                break
        if not script_running:
            subprocess.Popen(
                [sys.executable, os.path.join(os.path.dirname(__file__), 'ArduinoSerial.py')],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        app.run(debug=True)
    except Exception as e:
        print(f"Could not start ArduinoSerial.py: {e}")
