import pytest
from app.services.auth_service import users_by_email

def test_register_student_success(client):
    data = {
        "first_name": "Анна",
        "last_name": "Петрова",
        "email": "anna@test.ru",
        "password": "123",
        "group_id": 1
    }
    resp = client.post("/auth/register/student", json=data)
    assert resp.status_code == 201
    assert "user_id" in resp.json

def test_register_student_duplicate(client, sample_student):
    data = {
        "first_name": "Иван",
        "last_name": "Иванов",
        "email": "student@test.ru",  # уже есть
        "password": "123",
        "group_id": 1
    }
    resp = client.post("/auth/register/student", json=data)
    assert resp.status_code == 409

def test_login_success(client, sample_student):
    resp = client.post("/auth/login", json={"email": "student@test.ru", "password": "123"})
    assert resp.status_code == 200
    assert "token" in resp.json
    assert "user" in resp.json
    assert resp.json["user"]["role"] == "student"

def test_login_invalid(client):
    resp = client.post("/auth/login", json={"email": "no@no.ru", "password": "123"})
    assert resp.status_code == 401