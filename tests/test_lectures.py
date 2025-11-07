import pytest
from app.services.auth_service import generate_jwt_token
def test_get_lectures_student_success(client, sample_student):
    token = generate_jwt_token(sample_student)
    resp = client.get("/api/lectures", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert isinstance(resp.json, list)
    # Студент из группы 1 должен видеть только лекции группы 1
    assert len([l for l in resp.json if l["group"]["id"] == 1]) >= 1
    assert all(l["group"]["id"] == 1 for l in resp.json)

def test_get_lectures_teacher_success(client, sample_teacher):
    token = generate_jwt_token(sample_teacher)
    resp = client.get("/api/lectures", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert isinstance(resp.json, list)
    # Препод видит все лекции
    assert len(resp.json) >= 2