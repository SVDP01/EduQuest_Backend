import jwt
import time
from typing import Optional, Dict
from app.config import Config
from app.models import User, Group

# 🔒 Заглушечные БД в памяти
users_db: Dict[int, User] = {}
users_by_email: Dict[str, User] = {}
next_user_id = 1

groups_db = {
    1: Group(id=1, name="МАТ-101", faculty="Математический факультет")
}

def _hash_password(password: str) -> str:
    # Для заглушки — просто возвращаем как есть
    return password

def register_student(
    first_name: str, last_name: str, email: str, password: str, group_id: int
) -> Optional[User]:
    global next_user_id
    if email in users_by_email:
        return None  # conflict
    group = groups_db.get(group_id)
    if not group:
        return None  # invalid group (в реальности — 400)
    user = User(
        id=next_user_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=_hash_password(password),
        role="student",
        group=group
    )
    users_db[user.id] = user
    users_by_email[user.email] = user
    next_user_id += 1
    return user

def register_teacher(
    first_name: str, last_name: str, email: str, password: str, department: str
) -> Optional[User]:
    global next_user_id
    if email in users_by_email:
        return None
    user = User(
        id=next_user_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=_hash_password(password),
        role="teacher",
        department=department
    )
    users_db[user.id] = user
    users_by_email[user.email] = user
    next_user_id += 1
    return user

def authenticate_user(email: str, password: str) -> Optional[User]:
    user = users_by_email.get(email)
    if user and user.password_hash == password:  # заглушка
        return user
    return None

def generate_jwt_token(user: User) -> str:
    payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": int(time.time()) + Config.JWT_EXP_DELTA_SECONDS
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

def decode_jwt_token(token: str) -> Optional[Dict]:
    try:
        return jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_user_by_id(user_id: int) -> Optional[User]:
    return users_db.get(user_id)

# После register_teacher добавьте:
def register_admin(first_name: str, last_name: str, email: str, password: str):
    global next_user_id
    if email in users_by_email:
        return None
    user = User(
        id=next_user_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=_hash_password(password),
        role="admin"
    )
    users_db[user.id] = user
    users_by_email[user.email] = user
    next_user_id += 1
    return user