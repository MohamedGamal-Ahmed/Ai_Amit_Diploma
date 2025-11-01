import streamlit as st
import numpy as np
import joblib

# تحميل الموديل
reg = joblib.load('reg.pkl')

st.title("🏡 Boston House Price Prediction")

rm = st.number_input("Number of Rooms (RM):", min_value=1.0, step=0.1)
lstat = st.number_input("Poverty Level (%) (LSTAT):", min_value=0.0, step=0.1)
ptratio = st.number_input("Student-Teacher Ratio (PTRATIO):", min_value=5.0, step=0.1)

if st.button("Predict"):
    features = np.array([[rm, lstat, ptratio]])
    price = reg.predict(features)[0]
    st.success(f"🏠 Estimated Price: ${price:,.2f}")
