import streamlit as st
import numpy as np
import joblib
import json
from tensorflow import keras

# =========================
# Page Config
# =========================
st.set_page_config(page_title=" Boston Housing ML & DL Dashboard", page_icon="", layout="centered")

st.title(" Boston Housing Price Prediction Dashboard")
st.markdown("""
Explore and compare predictions between:
-  Traditional **Machine Learning Model**
-  **Deep Learning Neural Network Model**
""")

# =========================
# Tabs Navigation
# =========================
tab1, tab2 = st.tabs([" Machine Learning Model", " Neural Network Model"])

# =========================
# TAB 1: MACHINE LEARNING MODEL
# =========================
with tab1:
    st.header(" Predict Using Traditional ML Model")

    try:
        reg = joblib.load("reg.pkl")
        st.success(" ML model loaded successfully.")

        rm = st.number_input("Average number of rooms (RM):", min_value=1.0, step=0.1)
        lstat = st.number_input("Lower status population (%) (LSTAT):", min_value=0.0, step=0.1)
        ptratio = st.number_input("Pupil-teacher ratio (PTRATIO):", min_value=5.0, step=0.1)

        if st.button("Predict (ML Model)"):
            features = np.array([[rm, lstat, ptratio]])
            price = reg.predict(features)[0]
            st.success(f" Predicted House Price: ${price:,.2f}")

    except Exception as e:
        st.error(f" Error loading ML model: {e}")

# =========================
# TAB 2: NEURAL NETWORK MODEL
# =========================
with tab2:
    st.header(" Predict Using Neural Network Model")

    try:
        # Load NN model and scalers
        model = keras.models.load_model("model_outputs/nn_model.keras")
        scaler_X = joblib.load("model_outputs/scaler_X.pkl")
        scaler_y = joblib.load("model_outputs/scaler_y.pkl")

        with open("model_outputs/metrics.json", "r") as f:
            metrics = json.load(f)

        st.success(" Neural Network model and data loaded successfully.")

        rm = st.number_input("Average number of rooms (RM)", min_value=1.0, step=0.1, key="nn_rm")
        lstat = st.number_input("Lower status population (%) (LSTAT)", min_value=0.0, step=0.1, key="nn_lstat")
        ptratio = st.number_input("Pupil-teacher ratio (PTRATIO)", min_value=5.0, step=0.1, key="nn_ptratio")

        if st.button("Predict (NN Model)"):
            input_data = np.array([[rm, lstat, ptratio]])
            input_scaled = scaler_X.transform(input_data)
            pred_scaled = model.predict(input_scaled, verbose=0)
            pred = scaler_y.inverse_transform(pred_scaled)

            st.success(f" Predicted House Price: ${pred[0][0]:,.2f}")

            # Show metrics
            st.subheader("Model Performance Summary")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Train MAE", f"{metrics['train_mae']:,.2f}")
            col2.metric("Test MAE", f"{metrics['test_mae']:,.2f}")
            col3.metric("Test RMSE", f"{metrics['test_rmse']:,.2f}")
            col4.metric("Epochs Trained", metrics['epochs_trained'])

            # Training curves
            st.subheader(" Training Curves")
            st.image("model_outputs/training_results.png", use_container_width=True)

    except Exception as e:
        st.error(f" Error loading Neural Network model: {e}")
