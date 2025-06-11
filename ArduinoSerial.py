import serial
import time
import sys
import json
sys.path.append(r"e:\Computer Programming\SDP Project")
from mlp_predict import mlp_predict  # Use your new MLP prediction function

# Setup serial connection
arduino = serial.Serial('COM3', 115200)  # Change to your Arduino port
time.sleep(2)  # Let Arduino initialize

# Thresholds
# soil_threshold = 500  # Adjust this after calibration

while True:
    try:
        line = arduino.readline().decode('utf-8').strip()
        if line.startswith("Soil:"):
            print(f"Received: {line}")

            # Parse values
            parts = line.split(',')
            soil = int(parts[0].split(':')[1])
            soil_percent = 100 - (0 - soil) / (0 - 1023) * 100
            print(f"Soil Moisture Percent: {soil_percent:.2f}%")
            temp = float(parts[1].split(':')[1])
            hum = float(parts[2].split(':')[1])

            print(f"Soil: {soil}, Temp: {temp}°C, Hum: {hum}%")

            # Use MLP model for relay logic
            status = mlp_predict(soil, temp, hum)
            print(f"MLP Prediction: {status}")
            if status == 0:
                print("Soil is dry — turning water ON")
                arduino.write(b'1')  # Turn ON relay
            else:
                print("Soil is wet — turning water OFF")
                arduino.write(b'0')  # Turn OFF relay

            # Save data to JSON file
            data = {
                "soil": soil_percent,
                "temp": temp,
                "hum": hum,
                "pump": "ON" if status == 0 else "OFF"
            }
            with open("sensor_data.json", "w") as f:
                json.dump(data, f)

        time.sleep(1.4)  # Adjust delay as needed

    except KeyboardInterrupt:
        print("Stopped by user")
        arduino.write(b'0')  # Ensure relay is OFF
        break
    except serial.SerialException as e:
        print(f"SerialException: {e}")
        # arduino.write(b'0')  # Ensure relay is OFF
        sys.exit(1)
    except Exception as e:
        print("Error:", e)
