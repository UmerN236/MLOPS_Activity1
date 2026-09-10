import os
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)

DEFAULT_APP_VERSION = Path("VERSION").read_text().strip()
APPLICATION_VERSION = os.getenv("APP_VERSION", DEFAULT_APP_VERSION)
MODEL_VERSION = os.getenv("MODEL_VERSION", "model-7")


@app.get("/")
def home():
    return jsonify(
        service="mlops-demo",
        status="running",
    )


@app.get("/health")
def health():
    return jsonify(
        application_version=APPLICATION_VERSION,
        model_version=MODEL_VERSION,
        status="healthy",
    )


@app.post("/predict")
def predict():
    data = request.get_json()

    if not data or "value" not in data:
        return jsonify(error="JSON field 'value' is required"), 400

    try:
        value = float(data["value"])
    except (TypeError, ValueError):
        return jsonify(error="'value' must be numeric"), 400

    # Dummy ML prediction for this activity
    prediction = value * 2

    return jsonify(
        input=value,
        prediction=prediction,
        model_version=MODEL_VERSION,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)