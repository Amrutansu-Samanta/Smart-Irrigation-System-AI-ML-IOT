import numpy as np
import pickle
import tensorflow as tf

# Load scaler and model once
with open('mlp_scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
model = tf.keras.models.load_model('mlp_model.keras')

def mlp_predict(soil, temp, hum):
    input_data = np.array([[soil, temp, hum]])
    input_scaled = scaler.transform(input_data)
    pred = model.predict(input_scaled)
    return int(pred[0][0] > 0.5)  # 1 for ON, 0 for OFF