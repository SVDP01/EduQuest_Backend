import pytest
from app.services.auth_service import generate_jwt_token
def test_solve_problem_student_success(client, sample_teacher, sample_student):
    # Создаём задачу
    token_t = generate_jwt_token(sample_teacher)
    resp = client.post("/api/trainer/problems",
        json={
            "text": "Решите уравнение x + 2 = 5",
            "difficulty": "easy",
            "subject": "Математика",
            "solution_steps": ["x = 5 - 2", "x = 3"],
            "correct_answer": "3"
        },
        headers={"Authorization": f"Bearer {token_t}"}
    )
    assert resp.status_code == 201
    problem_id = resp.json["id"]

    token_s = generate_jwt_token(sample_student)
    resp = client.post(f"/api/trainer/problems/{problem_id}/solve",
        json={"answer": "3"},
        headers={"Authorization": f"Bearer {token_s}"}
    )
    assert resp.status_code == 200
    assert resp.json["is_correct"] is True
    assert resp.json["points_earned"] == 5


