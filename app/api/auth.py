from flask_restx import Namespace, Resource, fields
from app.services.auth_service import (
    register_student,
    register_teacher,
    authenticate_user,
    generate_jwt_token
)

api = Namespace("Authentication", description="Аутентификация и регистрация")

# Модели для валидации и документации
student_reg_model = api.model("StudentRegistration", {
    "first_name": fields.String(required=True, example="Иван"),
    "last_name": fields.String(required=True, example="Иванов"),
    "email": fields.String(required=True, example="ivan@university.edu"),
    "password": fields.String(required=True, example="password123"),
    "group_id": fields.Integer(required=True, example=1)
})

teacher_reg_model = api.model("TeacherRegistration", {
    "first_name": fields.String(required=True, example="Петр"),
    "last_name": fields.String(required=True, example="Петров"),
    "email": fields.String(required=True, example="petr@university.edu"),
    "password": fields.String(required=True, example="password123"),
    "department": fields.String(required=True, example="Математический факультет")
})

login_model = api.model("Login", {
    "email": fields.String(required=True, example="ivan@university.edu"),
    "password": fields.String(required=True, example="password123")
})

login_response_model = api.model("LoginResponse", {
    "token": fields.String(example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
    "user": fields.Raw()
})

@api.route("/register/student")
class StudentRegister(Resource):
    @api.expect(student_reg_model)
    @api.response(201, "Создан")
    @api.response(400, "Некорректные данные")
    @api.response(409, "Пользователь существует")
    def post(self):
        data = api.payload
        user = register_student(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
            group_id=data["group_id"]
        )
        if not user:
            api.abort(409, "Пользователь с таким email уже существует")
        return {"message": "Студент успешно зарегистрирован", "user_id": user.id}, 201

@api.route("/register/teacher")
class TeacherRegister(Resource):
    @api.expect(teacher_reg_model)
    @api.response(201, "Создан")
    @api.response(409, "Пользователь существует")
    def post(self):
        data = api.payload
        user = register_teacher(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
            department=data["department"]
        )
        if not user:
            api.abort(409, "Пользователь с таким email уже существует")
        return {"message": "Преподаватель успешно зарегистрирован", "user_id": user.id}, 201

@api.route("/login")
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, "Успешно", login_response_model)
    @api.response(401, "Неверные учётные данные")
    def post(self):
        data = api.payload
        user = authenticate_user(data["email"], data["password"])
        if not user:
            api.abort(401, "Неверный email или пароль")
        token = generate_jwt_token(user)
        return {
            "token": token,
            "user": user.to_dict()
        }, 200