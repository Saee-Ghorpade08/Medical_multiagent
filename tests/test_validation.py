from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_ask_rejects_short_question():
    response = client.post("/ask", json={"question": "hi"})
    assert response.status_code == 422


def test_ask_rejects_blank_question():
    response = client.post("/ask", json={"question": "   "})
    assert response.status_code == 422
