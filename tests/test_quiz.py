import pytest
from app.services.auth_service import generate_jwt_token

def test_create_quiz_question_teacher_success(client, sample_teacher):
    token = generate_jwt_token(sample_teacher)
    resp = client.post("/api/quiz/questions",
        json={
            "text": "2+2=?",
            "options": ["3", "4", "5"],
            "correct_answer": 1,
            "points": 10
        },
        headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    assert resp.json["text"] == "2+2=?"

def test_submit_quiz_success(client, sample_teacher, sample_student):
    # 1. Создаём вопрос (от препода)
    token_t = generate_jwt_token(sample_teacher)
    client.post("/api/quiz/questions",
        json={
            "text": "2+2=?",
            "options": ["3", "4", "5"],
            "correct_answer": 1
        },
        headers={"Authorization": f"Bearer {token_t}"})

    # 2. Студент проходит викторину
    token_s = generate_jwt_token(sample_student)
    resp = client.post("/api/quiz/submit",
        json=[
            {"question_id": 1, "selected_option_index": 1}
        ],
        headers={"Authorization": f"Bearer {token_s}"})
    
    assert resp.status_code == 200
    assert resp.json["earned_points"] == 10
    assert resp.json["correct_answers"] == 1

    resp = client.get(f"/api/users/{sample_student.id}/points", headers={"Authorization": f"Bearer {token_s}"})
    assert resp.status_code == 200
    assert resp.json["points"] == 10