### Технологический стек
Python 3.13 + Flask + Flask-RESTx + PyJWT

### Роли
- `student` — студент
- `teacher` — преподаватель
- `admin` — администратор

### Аутентификация
JWT (HS256)

### Покрытие API
100% (`swagger.yml`, OpenAPI 3.0)

---

## Быстрое развертывание

### Требования
- Python ≥ 3.9  
- `venv` (входит в дистрибутив Python)

### Установка и запуск

```bash
# 1. Клонировать (если нужно)
git clone https://github.com/SVDP01/EduQuest_Backend.git
cd EduQuest_Backend

# 2. Создать и активировать виртуальное окружение
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Запустить сервер
python run.py
```
### Структура
EduQuest_Backend/
> app/
>> __init__.py          # Flask + RESTX инициализация
>> config.py            # Конфигурация (JWT_SECRET_KEY)
>> models/              # Dataclasses: User, Group, Question...
>> services/            # Бизнес-логика (заглушки)
>> api/                 # REST-эндпоинты (по модулям)
> tests/                   # Тесты (pytest)
> run.py                   # Точка входа
> requirements.txt         # Зависимости
> pytest.ini               # Конфиг pytest
> .gitignore               # Исключения для Git

### Тесты
```bash
# Все тесты
pytest

# Подробный вывод
pytest -v

# Только тесты викторин
pytest tests/test_quiz.py -v

```



