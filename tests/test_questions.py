import pytest
from app.services.auth_service import generate_jwt_token

def test_create_question_unauthorized(client):
    resp = client.post("/api/groups/1/questions", json={"text": "Q?"})
    assert resp.status_code == 401

def test_create_question_student_forbidden(client, sample_student):
    token = generate_jwt_token(sample_student)
    resp = client.post("/api/groups/1/questions",
                      json={"text": "Q?"},
                      headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403

def test_create_question_teacher_success(client, sample_teacher):
    token = generate_jwt_token(sample_teacher)
    resp = client.post("/api/groups/1/questions",
                      json={"text": "Можно повторить теорему?"},
                      headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    assert resp.json["text"] == "Можно повторить теорему?"
    assert "id" in resp.json

def test_get_questions_success(client, sample_teacher, sample_student):
    # Создаём вопрос от препода
    token_t = generate_jwt_token(sample_teacher)
    resp = client.post("/api/groups/1/questions",
                      json={"text": "Тестовый вопрос"},
                      headers={"Authorization": f"Bearer {token_t}"})
    assert resp.status_code == 201
    question_id = resp.json["id"]

    # Студент получает список
    token_s = generate_jwt_token(sample_student)
    resp = client.get("/api/groups/1/questions", headers={"Authorization": f"Bearer {token_s}"})
    assert resp.status_code == 200
    questions = resp.json
    # Ищем вопрос с нужным id
    found = any(q["id"] == question_id for q in questions)
    assert found, f"Вопрос с id={question_id} не найден в списке: {[q['id'] for q in questions]}"

