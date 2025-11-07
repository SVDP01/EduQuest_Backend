from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.quiz_service import (
    create_quiz_question, get_all_quiz_questions,
    submit_quiz_answers, get_user_points
)
from app.models.quiz_answer import QuizAnswer
from app.services.auth_service import decode_jwt_token

api = Namespace("Quiz", description="Викторины и баллы")

# Модели
quiz_question_model = api.model("QuizQuestion", {
    "text": fields.String(required=True, example="Что такое производная?"),
    "options": fields.List(fields.String, required=True, example=["Предел", "Интеграл", "Дифференциал"]),
    "correct_answer": fields.Integer(required=True, min=0, example=0),
    "points": fields.Integer(default=10, example=10)
})

quiz_answer_model = api.model("QuizAnswer", {
    "question_id": fields.Integer(required=True, example=1),
    "selected_option_index": fields.Integer(required=True, min=0, example=0)
})

quiz_result_model = api.model("QuizResult", {
    "total_points": fields.Integer(example=50),
    "correct_answers": fields.Integer(example=4),
    "total_questions": fields.Integer(example=5),
    "earned_points": fields.Integer(example=40)
})
points_model = api.model("Points", {
    "points": fields.Integer(example=150)
})
@api.route("/quiz/questions")
class QuizQuestions(Resource):
    @api.doc(security="BearerAuth")
    @api.expect(quiz_question_model)
    @api.response(201, "Вопрос создан")
    @api.response(403, "Только преподаватели")
    def post(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            api.abort(401)
        token = auth_header.split(" ")[1]
        payload = decode_jwt_token(token)
        if not payload or payload["role"] != "teacher":
            api.abort(403)

        data = api.payload
        try:
            question = create_quiz_question(**{
                k: v for k, v in data.items()
                if k in ["text", "options", "correct_answer", "points"]
            })
        except ValueError as e:
            api.abort(400, str(e))
        return question.to_dict(include_correct=True), 201

@api.route("/quiz")
class Quiz(Resource):
    @api.doc(security="BearerAuth")
    @api.response(200, "Вопросы викторины", [quiz_question_model])
    def get(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            api.abort(401)
        token = auth_header.split(" ")[1]
        payload = decode_jwt_token(token)
        if not payload:
            api.abort(401)

        questions = get_all_quiz_questions()
        return [q.to_dict() for q in questions], 200

@api.route("/quiz/submit")
class QuizSubmit(Resource):
    @api.doc(security="BearerAuth")
    @api.expect([quiz_answer_model])
    @api.response(200, "Результат", quiz_result_model)
    def post(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            api.abort(401)
        token = auth_header.split(" ")[1]
        payload = decode_jwt_token(token)
        if not payload or payload["role"] != "student":
            api.abort(403)

        answers = []
        for item in api.payload:
            answers.append(QuizAnswer(
                question_id=item["question_id"],
                selected_option_index=item["selected_option_index"]
            ))

        result = submit_quiz_answers(payload["user_id"], answers)
        return {
            "total_points": result.total_points,
            "correct_answers": result.correct_answers,
            "total_questions": result.total_questions,
            "earned_points": result.earned_points
        }, 200

@api.route("/users/<int:user_id>/points")
class UserPoints(Resource):
    @api.doc(security="BearerAuth")
    @api.marshal_with(points_model)  # ✅ явно указываем модель
    @api.response(200, "Баллы")
    @api.response(401, "Неавторизован")
    @api.response(403, "Доступ запрещён")
    def get(self, user_id):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            api.abort(401)
        token = auth_header.split(" ")[1]
        payload = decode_jwt_token(token)
        if not payload:
            api.abort(401)

        # Студент может смотреть только себя, препод/админ — всех
        if payload["role"] == "student" and payload["user_id"] != user_id:
            api.abort(403)

        points = get_user_points(user_id)
        return {"points": points}, 200