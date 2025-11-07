import pytest
from app.services.auth_service import generate_jwt_token

def test_get_me_success(client, sample_student):
    token = generate_jwt_token(sample_student)
    resp = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json["id"] == sample_student.id
    assert resp.json["email"] == sample_student.email

def test_get_me_no_token(client):
    resp = client.get("/api/users/me")
    assert resp.status_code == 401

def test_get_me_invalid_token(client):
    resp = client.get("/api/users/me", headers={"Authorization": "Bearer invalid.token.here"})
    assert resp.status_code == 401