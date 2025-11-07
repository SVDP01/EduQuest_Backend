from typing import List, Optional, Tuple
from datetime import datetime
from app.models.question import Question
from app.models.answer import Answer

# Заглушечные БД
_questions_db = {}
_answers_db = []
_next_question_id = 1
_next_answer_id = 1

def create_question(text: str, teacher_id: int, group_id: int) -> Question:
    global _next_question_id
    question = Question(
        id=_next_question_id,
        text=text,
        teacher_id=teacher_id,
        group_id=group_id,
        created_at=datetime.utcnow()
    )
    _questions_db[question.id] = question
    _next_question_id += 1
    return question

def get_questions_by_group(group_id: int, page: int = 1, limit: int = 20) -> Tuple[List[Question], int]:
    questions = [q for q in _questions_db.values() if q.group_id == group_id]
    total = len(questions)
    start = (page - 1) * limit
    end = start + limit
    return questions[start:end], total

def delete_question(question_id: int, teacher_id: int) -> bool:
    question = _questions_db.get(question_id)
    if not question or question.teacher_id != teacher_id:
        return False
    del _questions_db[question_id]
    # Опционально: удалить ответы (для MVP — оставим)
    return True

def create_answer(text: str, student_id: int, question_id: int) -> Optional[Answer]:
    if question_id not in _questions_db:
        return None
    global _next_answer_id
    answer = Answer(
        id=_next_answer_id,
        text=text,
        student_id=student_id,
        question_id=question_id,
        created_at=datetime.utcnow()
    )
    _answers_db.append(answer)
    _next_answer_id += 1
    return answer

def get_answers_by_question(question_id: int, page: int = 1, limit: int = 20) -> Tuple[List[Answer], int]:
    answers = [a for a in _answers_db if a.question_id == question_id]
    total = len(answers)
    start = (page - 1) * limit
    end = start + limit
    return answers[start:end], total
# Для тестов — экспорт внутреннего состояния
__all__ = [
    "create_question", "get_questions_by_group", "delete_question",
    "create_answer", "get_answers_by_question",
    "_questions_db", "_answers_db", "_next_question_id", "_next_answer_id"
]