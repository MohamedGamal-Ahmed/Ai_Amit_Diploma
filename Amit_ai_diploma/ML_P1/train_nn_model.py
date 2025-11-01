import os
import json
import matplotlib.pyplot as plt
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib
import numpy as np

# ===============================
# 1.  loading data
# ===============================
print(" Loading data...")
data = pd.read_csv("C:/Users/Mgama/Ai_Amit_Diploma/Amit_ai_diploma/ML_P1/housing.csv")




print(f"Dataset shape: {data.shape}")
print(f"Target (MEDV) mean: {data['MEDV'].mean():.2f}")


X = data[["RM", "LSTAT", "PTRATIO"]]
y = data["MEDV"]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ===============================
# 2. Scaling data
# ===============================
scaler_X = StandardScaler()
X_train_scaled = scaler_X.fit_transform(X_train)
X_test_scaled = scaler_X.transform(X_test)


scaler_y = StandardScaler()
y_train_scaled = scaler_y.fit_transform(y_train.values.reshape(-1, 1)).flatten()
y_test_scaled = scaler_y.transform(y_test.values.reshape(-1, 1)).flatten()

# ===============================
# 3. Building the Neural Network Model
# ===============================
print("\n Building model...")

model = keras.Sequential([
    keras.Input(shape=(3,)),
    keras.layers.Dense(32, activation="relu", kernel_regularizer=keras.regularizers.l2(0.001)),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(16, activation="relu", kernel_regularizer=keras.regularizers.l2(0.001)),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(8, activation="relu"),
    keras.layers.Dense(1)
])

optimizer = keras.optimizers.Adam(learning_rate=0.01)
model.compile(optimizer=optimizer, loss="mse", metrics=["mae"])

print(model.summary())

# ===============================
# 4. Callbacks & Training
# ===============================
callbacks = [
    keras.callbacks.EarlyStopping(monitor="val_loss", patience=20, restore_best_weights=True, verbose=1),
    keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=10, min_lr=0.0001, verbose=1)
]

# ===============================
# 5. Training the model
# ===============================
print("\n Training model...")
history = model.fit(
    X_train_scaled, y_train_scaled,  #   y_train_scaled
    validation_data=(X_test_scaled, y_test_scaled),  #   y_test_scaled
    epochs=300,
    batch_size=16,
    callbacks=callbacks,
    verbose=1
)

# ===============================
# 6. Evaluating the model
# ===============================
print("\n Evaluating model...")

# inverse transform
y_train_pred_scaled = model.predict(X_train_scaled, verbose=0).flatten()
y_test_pred_scaled = model.predict(X_test_scaled, verbose=0).flatten()

#  scaling
y_train_pred = scaler_y.inverse_transform(y_train_pred_scaled.reshape(-1, 1)).flatten()
y_test_pred = scaler_y.inverse_transform(y_test_pred_scaled.reshape(-1, 1)).flatten()


train_mae = np.mean(np.abs(y_train - y_train_pred))
test_mae = np.mean(np.abs(y_test - y_test_pred))
train_loss = np.mean((y_train - y_train_pred)**2)
test_loss = np.mean((y_test - y_test_pred)**2)

print(f"\n{'='*50}")
print(f" TRAIN RESULTS: MAE=${train_mae:.2f}, MSE=${train_loss:.2f}")
print(f" TEST RESULTS: MAE=${test_mae:.2f}, MSE=${test_loss:.2f}")
print(f"RMSE (Test): ${np.sqrt(test_loss):.2f}")
print(f"{'='*50}\n")

# ===============================
# 7. Saving Model, Scalers, Metrics & Plots
# ===============================
output_dir = "model_outputs"
os.makedirs(output_dir, exist_ok=True)


model.save(os.path.join(output_dir, "nn_model.keras"))
joblib.dump(scaler_X, os.path.join(output_dir, "scaler_X.pkl"))
joblib.dump(scaler_y, os.path.join(output_dir, "scaler_y.pkl"))  

# history
np.save(os.path.join(output_dir, "history.npy"), history.history)

# metrics
metrics = {
    "train_mae": float(train_mae),
    "train_mse": float(train_loss),
    "train_rmse": float(np.sqrt(train_loss)),
    "test_mae": float(test_mae),
    "test_mse": float(test_loss),
    "test_rmse": float(np.sqrt(test_loss)),
    "epochs_trained": len(history.history["loss"])
}
with open(os.path.join(output_dir, "metrics.json"), "w") as f:
    json.dump(metrics, f, indent=4)

# ===============================
# 8. Plotting Training History
# ===============================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Loss
axes[0].plot(history.history["loss"], label="Train Loss")
axes[0].plot(history.history["val_loss"], label="Validation Loss")
axes[0].set_title("Loss Curve (MSE)")
axes[0].set_xlabel("Epochs")
axes[0].set_ylabel("MSE")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# MAE
axes[1].plot(history.history["mae"], label="Train MAE")
axes[1].plot(history.history["val_mae"], label="Validation MAE")
axes[1].set_title("MAE Curve")
axes[1].set_xlabel("Epochs")
axes[1].set_ylabel("MAE")
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "training_results.png"), dpi=300)
plt.close()

print(f" Model, Scalers, Metrics & Plots saved in: {os.path.abspath(output_dir)}")

