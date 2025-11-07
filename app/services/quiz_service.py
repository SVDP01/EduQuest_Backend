from typing import List, Optional
from app.models.quiz_question import QuizQuestion
from app.models.quiz_answer import QuizAnswer, QuizResult
from app.services.auth_service import get_user_by_id, users_db

# Заглушечная БД
_quiz_questions_db = {}
_next_question_id = 1

def create_quiz_question(text: str, options: List[str], correct_answer: int, points: int = 10) -> QuizQuestion:
    global _next_question_id
    if not (0 <= correct_answer < len(options)):
        raise ValueError("correct_answer выходит за пределы options")
    question = QuizQuestion(
        id=_next_question_id,
        text=text,
        options=options,
        correct_answer=correct_answer,
        points=points
    )
    _quiz_questions_db[question.id] = question
    _next_question_id += 1
    return question

def get_all_quiz_questions() -> List[QuizQuestion]:
    return list(_quiz_questions_db.values())

def submit_quiz_answers(student_id: int, answers: List[QuizAnswer]) -> QuizResult:
    questions = get_all_quiz_questions()
    question_map = {q.id: q for q in questions}
    
    correct = 0
    earned = 0
    for ans in answers:
        q = question_map.get(ans.question_id)
        if q and ans.selected_option_index == q.correct_answer:
            correct += 1
            earned += q.points

    # Начисляем баллы студенту
    user = get_user_by_id(student_id)
    if user:
        user.points += earned
        users_db[user.id] = user  # обновляем в "БД" (для заглушки)

    return QuizResult(
        total_points=sum(q.points for q in questions),
        correct_answers=correct,
        total_questions=len(questions),
        earned_points=earned
    )

def get_user_points(user_id: int) -> int:
    user = get_user_by_id(user_id)
    return user.points if user else 0