from collections import defaultdict
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import joblib

data = []
with open('training_data.txt', 'r') as f:
    for line in f:
        try:

            entries = json.loads(line.strip())
            if isinstance(entries, list): 
                data.extend(entries)  
            else:
                print(f"Skipping non-list entry: {entries}")
        except json.JSONDecodeError:
            print(f"Skipping invalid line: {line.strip()}")  

aggregated_data = defaultdict(list)
for entry in data:
    try:
        state_vector = tuple(entry["state_vector"]) 
        aggregated_data[state_vector].append(reward)
    except KeyError:
        print(f"Skipping entry due to missing key: {entry}")


averaged_data = {k: sum(v) / len(v) for k, v in aggregated_data.items()}

with open("aggregated_training_data.txt", "w") as f:
    for state_vector, avg_reward in averaged_data.items():
        f.write(f"{list(state_vector)} {avg_reward}\n")

 
X = np.array(list(averaged_data.keys()))
y = np.array(list(averaged_data.values()))

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_temp, y_train, y_temp = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)  # Single output for regression
])


model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError(), metrics=['mae'])

history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=100,
    batch_size=5,
    verbose=1
)

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('trained_model.tflite', 'wb') as f:
    f.write(tflite_model)
    
joblib.dump(scaler, 'scaler.pkl')



