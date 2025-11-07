import pytest
from app.services.auth_service import generate_jwt_token

def test_create_reward_non_admin_forbidden(client, sample_teacher):
    token = generate_jwt_token(sample_teacher)
    resp = client.post("/api/rewards",
        json={"name": "Кружка", "cost": 50},
        headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403

def test_create_reward_admin_success(client, sample_admin):
    token = generate_jwt_token(sample_admin)
    resp = client.post("/api/rewards",
        json={
            "name": "Футболка",
            "description": "Хлопковая",
            "cost": 100,
            "category": "merch"
        },
        headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    assert resp.json["name"] == "Футболка"
    assert resp.json["cost"] == 100

def test_get_rewards_success(client, sample_student):
    token = generate_jwt_token(sample_student)
    resp = client.get("/api/rewards", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert isinstance(resp.json, list)