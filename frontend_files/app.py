# Streamlit frontend for the SuperKart sales forecasting model
import os
import requests
import pandas as pd
import streamlit as st

# Set BACKEND_URL as a Space variable, or edit the default below
BACKEND_URL = os.getenv("BACKEND_URL", "https://<your-username>-superkart-backend.hf.space").rstrip("/")

st.set_page_config(page_title="SuperKart Sales Forecast", layout="centered")
st.title("SuperKart Sales Forecast")
st.write("Predict the total sales of a product in a store, one at a time or in bulk.")

st.subheader("Online prediction (single)")
c1, c2 = st.columns(2)
with c1:
    product_weight = st.number_input("Product Weight", 0.0, 50.0, 12.5, 0.01)
    sugar = st.selectbox("Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
    area = st.number_input("Allocated Display Area (ratio)", 0.0, 1.0, 0.07, 0.001, format="%.3f")
    mrp = st.number_input("Product MRP", 0.0, 500.0, 147.0, 0.01)
    id_char = st.selectbox("Product ID prefix", ["FD", "NC", "DR"])
    category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])
with c2:
    store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
    city = st.selectbox("City Tier", ["Tier 1", "Tier 2", "Tier 3"])
    store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
    store_age = st.number_input("Store Age (years)", 0, 100, 16, 1)

if st.button("Predict Sales"):
    payload = {
        "Product_Weight": product_weight, "Product_Sugar_Content": sugar,
        "Product_Allocated_Area": area, "Product_MRP": mrp, "Store_Size": store_size,
        "Store_Location_City_Type": city, "Store_Type": store_type,
        "Product_Id_char": id_char, "Store_Age_Years": store_age,
        "Product_Type_Category": category,
    }
    try:
        r = requests.post(f"{BACKEND_URL}/v1/predict", json=payload, timeout=60)
        if r.ok:
            st.success(f"Predicted sales: {r.json()['Predicted_Sales']:,.2f}")
        else:
            st.error(f"Backend error {r.status_code}: {r.text}")
    except requests.RequestException as e:
        st.error(f"Could not reach the backend: {e}")

st.subheader("Batch prediction")
up = st.file_uploader("Upload a CSV file", type=["csv"])
if up is not None and st.button("Predict for Batch"):
    try:
        r = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": (up.name, up.getvalue(), "text/csv")}, timeout=120)
        if r.ok:
            up.seek(0)
            out = pd.read_csv(up)
            out["Predicted_Sales"] = r.json()["Predicted_Sales"]
            st.dataframe(out)
            st.download_button("Download predictions", out.to_csv(index=False), "superkart_predictions.csv", "text/csv")
        else:
            st.error(f"Backend error {r.status_code}: {r.text}")
    except requests.RequestException as e:
        st.error(f"Could not reach the backend: {e}")
