import pytest
from app.services.auth_service import generate_jwt_token
def test_create_card_student_forbidden(client, sample_student):
    token = generate_jwt_token(sample_student)
    resp = client.post("/api/cards", json={"front_text":"Q", "back_text":"A"}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403

def test_create_card_teacher_success(client, sample_teacher):
    token = generate_jwt_token(sample_teacher)
    resp = client.post("/api/cards",
        json={"front_text":"Что такое предел?", "back_text":"...", "subject":"Матан", "topic":"Пределы"},
        headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    assert resp.json["subject"] == "Матан"

def test_get_cards_filter(client, sample_student):
    # ... (создать карточки от препода) ...
    token = generate_jwt_token(sample_student)
    resp = client.get("/api/cards?subject=Матан", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert len(resp.json) > 0