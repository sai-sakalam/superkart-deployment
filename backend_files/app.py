# Flask backend for the SuperKart sales forecasting model
import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask("SuperKart Sales Predictor")

# Load the serialized pipeline (preprocessing + tuned model)
model = joblib.load("SuperKart_model_v1_0.joblib")

FEATURES = [
    "Product_Weight", "Product_Sugar_Content", "Product_Allocated_Area", "Product_MRP",
    "Store_Size", "Store_Location_City_Type", "Store_Type",
    "Product_Id_char", "Store_Age_Years", "Product_Type_Category",
]


@app.get("/")
def home():
    return "Welcome to the SuperKart Sales Forecast API!"


@app.post("/v1/predict")
def predict():
    """Single prediction: expects one JSON object with the model features."""
    data = request.get_json(force=True)
    missing = [f for f in FEATURES if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400
    row = pd.DataFrame([{f: data[f] for f in FEATURES}])
    pred = float(model.predict(row)[0])
    return jsonify({"Predicted_Sales": round(pred, 2)})


@app.post("/v1/predictbatch")
def predict_batch():
    """Batch prediction: expects a CSV file upload under the key 'file'."""
    if "file" not in request.files:
        return jsonify({"error": "Upload a CSV under the key 'file'"}), 400
    df = pd.read_csv(request.files["file"])
    missing = [f for f in FEATURES if f not in df.columns]
    if missing:
        return jsonify({"error": f"Missing columns: {missing}"}), 400
    preds = model.predict(df[FEATURES]).round(2).tolist()
    return jsonify({"Predicted_Sales": preds})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=False)
