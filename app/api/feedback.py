from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.feedback_service import create_feedback
from app.services.auth_service import decode_jwt_token

api = Namespace("Feedback", description="Анонимное оценивание пары")

# Модель валидации
feedback_model = api.model("Feedback", {
    "rating": fields.Integer(
        required=True,
        min=1,
        max=5,
        example=4,
        description="Оценка от 1 до 5"
    ),
    "comment": fields.String(
        required=False,
        example="Хорошая лекция, но темп немного быстрый"
    ),
    "lecture_id": fields.Integer(
        required=True,
        example=101,
        description="ID лекции"
    )
})

@api.route("/feedback")
class Feedback(Resource):
    @api.doc(security="BearerAuth")
    @api.expect(feedback_model)
    @api.response(201, "Отзыв отправлен")
    @api.response(400, "Некорректные данные (rating 1–5)")
    @api.response(403, "Только студенты могут оценивать")
    @api.response(401, "Неавторизован")
    def post(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            api.abort(401, "Требуется аутентификация")
        token = auth_header.split(" ")[1]
        payload = decode_jwt_token(token)
        if not payload:
            api.abort(401, "Невалидный токен")
        
        user_id = payload["user_id"]
        role = payload["role"]
        if role != "student":
            api.abort(403, "Только студенты могут оставлять отзывы")
        
        data = api.payload
        rating = data.get("rating")
        comment = data.get("comment", "").strip()
        lecture_id = data.get("lecture_id")

        if not lecture_id:
            api.abort(400, "lecture_id обязателен")

        try:
            feedback = create_feedback(
                rating=rating,
                comment=comment,
                lecture_id=lecture_id,
                student_id=user_id
            )
        except ValueError as e:
            api.abort(400, str(e))

        # Возвращаем БЕЗ student_id — анонимно!
        return {"message": "Отзыв сохранён", "feedback_id": feedback.id}, 201