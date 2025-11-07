from typing import List
from datetime import datetime, timedelta
from app.models.lecture import Lecture
from app.models.group import Group
from app.models.user import User

# Заглушечная БД: 3 лекции
_lectures_db: List[Lecture] = []

def init_lectures():
    """Инициализация примеров лекций при старте (для заглушки)"""
    global _lectures_db
    if _lectures_db:
        return  # уже инициализировано

    # Группы для примера
    group1 = Group(id=1, name="МАТ-101", faculty="Матфак")
    group2 = Group(id=2, name="ИНФ-202", faculty="Факультет информатики")

    # Преподаватель
    teacher = User(id=101, first_name="Александр", last_name="Смирнов", 
                   email="a.smirnov@univ.ru", password_hash="***", 
                   role="teacher", department="Математика")

    now = datetime.utcnow()
    _lectures_db = [
        Lecture(
            id=1,
            title="Лекция 1: Введение в матанализ",
            description="Базовые понятия пределов и непрерывности",
            group=group1,
            teacher=teacher,
            scheduled_at=now + timedelta(days=1, hours=10),
            duration_minutes=90
        ),
        Lecture(
            id=2,
            title="Лекция 2: Производные",
            description="Определение, геометрический смысл, правила дифференцирования",
            group=group1,
            teacher=teacher,
            scheduled_at=now + timedelta(days=3, hours=10),
            duration_minutes=90
        ),
        Lecture(
            id=3,
            title="Лекция 1: Введение в Python",
            description="Переменные, типы, условия, циклы",
            group=group2,
            teacher=teacher,
            scheduled_at=now + timedelta(days=2, hours=12),
            duration_minutes=120
        )
    ]

def get_lectures_for_user(user) -> List[Lecture]:
    """Возвращает лекции по группе пользователя (студент) или все (препод/админ)"""
    init_lectures()
    if user.role == "student" and user.group:
        return [l for l in _lectures_db if l.group.id == user.group.id]
    else:
        return _lectures_db