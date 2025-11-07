import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from app import create_app
from app.services.auth_service import (
    register_student,
    register_teacher,
    register_admin,
    users_db,
    users_by_email,
    next_user_id
)
# Импортируем Group, чтобы создать заглушку для group_id=1
from app.models import Group

# --- Фикстура для сброса состояния перед каждым тестом ---
@pytest.fixture(autouse=True)
def reset_test_state():
    """Очищает все заглушечные 'БД' перед каждым тестом"""
    global next_user_id
    users_db.clear()
    users_by_email.clear()
    next_user_id = 1

# --- Приложение и клиент ---
@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# --- Фикстуры пользователей ---
@pytest.fixture
def sample_student():

    return register_student("Студент", "Тестов", "student@test.ru", "123", 1)

@pytest.fixture
def sample_teacher():
    return register_teacher("Препод", "Тестов", "teacher@test.ru", "123", "Факультет")

@pytest.fixture
def sample_admin():
    return register_admin("Админ", "Админов", "admin@test.ru", "123")


# Добавьте импорт в начало:
from app.services.question_service import _questions_db, _answers_db, _next_question_id, _next_answer_id
from app.services.group_service import _groups_db, _next_group_id
# В фикстуре reset_test_state:
@pytest.fixture(autouse=True)
def reset_test_state():
    """Очищает все заглушечные 'БД' перед каждым тестом"""
    global next_user_id, _next_group_id, _next_question_id, _next_answer_id

    # → Auth
    users_db.clear()
    users_by_email.clear()
    next_user_id = 1

    # → Groups
    _groups_db.clear()
    _groups_db.update({
        1: Group(id=1, name="МАТ-101", faculty="Математический факультет"),
        2: Group(id=2, name="ИНФ-202", faculty="Факультет информатики"),
    })
    _next_group_id = 3

    # → Questions & Answers
    _questions_db.clear()
    _answers_db.clear()
    _next_question_id = 1
    _next_answer_id = 1