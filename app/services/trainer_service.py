from typing import List
from app.models.problem import Problem
from app.services.auth_service import get_user_by_id, users_db

_problems_db = {}
_next_problem_id = 1

def create_problem(text: str, difficulty: str, subject: str, solution_steps: List[str], correct_answer: str) -> Problem:
    global _next_problem_id
    if difficulty not in ("easy", "medium", "hard"):
        raise ValueError("difficulty must be one of: easy, medium, hard")
    problem = Problem(
        id=_next_problem_id,
        text=text,
        difficulty=difficulty,
        subject=subject,
        solution_steps=solution_steps,
        correct_answer=correct_answer
    )
    _problems_db[problem.id] = problem
    _next_problem_id += 1
    return problem

def get_problems(difficulty: str = None, subject: str = None) -> List[Problem]:
    problems = list(_problems_db.values())
    if difficulty:
        problems = [p for p in problems if p.difficulty == difficulty]
    if subject:
        problems = [p for p in problems if p.subject.lower() == subject.lower()]
    return problems

def solve_problem(problem_id: int, user_answer: str, student_id: int) -> dict:
    problem = _problems_db.get(problem_id)
    if not problem:
        raise ValueError("Problem not found")

    is_correct = user_answer.strip().lower() == problem.correct_answer.strip().lower()
    points_earned = {"easy": 5, "medium": 10, "hard": 20}.get(problem.difficulty, 5) if is_correct else 0

    # Начисляем баллы
    user = get_user_by_id(student_id)
    if user and is_correct:
        user.points += points_earned
        users_db[user.id] = user
    result = {
        "is_correct": is_correct,
        "explanation": "Разбор решения:\n" + "\n".join(problem.solution_steps),
        "points_earned": points_earned
    }
    print("Returning result:", result)  # ← Добавьте эту строку
    return {
        "is_correct": is_correct,
        "explanation": "Разбор решения:\n" + "\n".join(problem.solution_steps),
        "points_earned": points_earned
    }


