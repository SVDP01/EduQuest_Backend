import pytest
from app.services.auth_service import generate_jwt_token

def test_feedback_unauthorized(client):
    resp = client.post("/api/feedback", json={"rating": 5, "lecture_id": 1})
    assert resp.status_code == 401

def test_feedback_teacher_forbidden(client, sample_teacher):
    token = generate_jwt_token(sample_teacher)
    resp = client.post("/api/feedback",
                      json={"rating": 5, "lecture_id": 1},
                      headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403

def test_feedback_student_success(client, sample_student):
    token = generate_jwt_token(sample_student)
    resp = client.post("/api/feedback",
                      json={"rating": 4, "comment": "Понравилось!", "lecture_id": 123},
                      headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    assert "feedback_id" in resp.json

def test_feedback_invalid_rating(client, sample_student):
    token = generate_jwt_token(sample_student)
    resp = client.post("/api/feedback",
                      json={"rating": 6, "lecture_id": 1},
                      headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 400