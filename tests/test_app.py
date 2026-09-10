from app import app


def test_health():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "application_version": "1.0.0",
        "model_version": "model-7",
        "status": "healthy",
    }


def test_prediction():
    client = app.test_client()
    response = client.post("/predict", json={"value": 5})

    assert response.status_code == 200
    assert response.get_json() == {
        "input": 5.0,
        "prediction": 10.0,
        "model_version": "model-7",
    }


def test_prediction_requires_value():
    client = app.test_client()
    response = client.post("/predict", json={})

    assert response.status_code == 400
    assert response.get_json() == {"error": "JSON field 'value' is required"}


def test_prediction_rejects_non_numeric_value():
    client = app.test_client()
    response = client.post("/predict", json={"value": "invalid"})

    assert response.status_code == 400
    assert response.get_json() == {"error": "'value' must be numeric"}
