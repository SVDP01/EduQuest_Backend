import pytest
from app.services.group_service import _groups_db
from app.services.auth_service import generate_jwt_token

@pytest.fixture(autouse=True)
def reset_groups_db():
    # Сбрасываем состояние перед каждым тестом
    global _groups_db
    from app.services.group_service import _groups_db
    _groups_db.clear()
    _groups_db.update({
        1: type('', (), {'id':1, 'name':"МАТ-101", 'faculty':"Матфак", 'to_dict':lambda s: {"id":1, "name":"МАТ-101", "faculty":"Матфак"}})()
    })

def test_get_groups_unauthorized(client):
    resp = client.get("/api/groups")
    assert resp.status_code == 401

def test_get_groups_success(client, sample_student):
    token = generate_jwt_token(sample_student)
    resp = client.get("/api/groups", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert isinstance(resp.json, list)
    assert len(resp.json) >= 1
    assert "МАТ-101" in [g["name"] for g in resp.json]

def test_get_groups_pagination(client, sample_student):
    token = generate_jwt_token(sample_student)
    resp = client.get("/api/groups?page=1&limit=1", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert len(resp.json) == 1

def test_create_group_unauthorized(client):
    resp = client.post("/api/groups", json={"name": "TEST", "faculty": "FAC"})
    assert resp.status_code == 401

def test_create_group_non_admin(client, sample_student):
    token = generate_jwt_token(sample_student)
    resp = client.post("/api/groups", 
                      json={"name": "ТЕСТ", "faculty": "Факультет"},
                      headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403
    assert "Только администраторы" in resp.json.get("message", "")

def test_create_group_admin_success(client, sample_admin):
    token = generate_jwt_token(sample_admin)
    resp = client.post("/api/groups",
                      json={"name": "МАТ-999", "faculty": "Новый факультет"},
                      headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    assert resp.json["name"] == "МАТ-999"
    assert resp.json["faculty"] == "Новый факультет"
    # Проверим, что добавилось
    get_resp = client.get("/api/groups", headers={"Authorization": f"Bearer {token}"})
    assert len(get_resp.json) > 1