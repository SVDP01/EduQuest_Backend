from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.question_service import (
    create_question, get_questions_by_group,
    delete_question, create_answer, get_answers_by_question
)
from app.services.auth_service import decode_jwt_token

api = Namespace("Questions", description="Вопросы во время пары")

# Модели
question_create_model = api.model("QuestionCreate", {
    "text": fields.String(required=True, example="Можно повторить доказательство?")
})

question_response_model = api.model("Question", {
    "id": fields.Integer(example=1),
    "text": fields.String(example="Можно повторить доказательство?"),
    "group_id": fields.Integer(example=1),
    "created_at": fields.String(example="2025-11-08T10:00:00Z"),
    "is_active": fields.Boolean(example=True)
})

answer_create_model = api.model("AnswerCreate", {
    "text": fields.String(required=True, example="Да, пожалуйста!")
})

answer_response_model = api.model("Answer", {
    "id": fields.Integer(example=1),
    "text": fields.String(example="Да, пожалуйста!"),
    "question_id": fields.Integer(example=1),
    "created_at": fields.String(example="2025-11-08T10:05:00Z")
})

def _get_auth_info():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        api.abort(401, "Требуется аутентификация")
    token = auth_header.split(" ")[1]
    payload = decode_jwt_token(token)
    if not payload:
        api.abort(401, "Невалидный токен")
    return payload["user_id"], payload["role"]

@api.route("/groups/<int:group_id>/questions")
class GroupQuestions(Resource):
    @api.doc(security="BearerAuth")
    @api.param("page", "Номер страницы", _in="query", type="integer", default=1)
    @api.param("limit", "Лимит", _in="query", type="integer", default=20)
    @api.response(200, "OK", [question_response_model])
    @api.response(401, "Неавторизован")
    def get(self, group_id):
        _, role = _get_auth_info()
        # Все авторизованные могут читать
        page = max(1, int(request.args.get("page", 1)))
        limit = min(100, max(1, int(request.args.get("limit", 20))))
        questions, total = get_questions_by_group(group_id, page=page, limit=limit)
        return [q.to_dict() for q in questions], 200

    @api.doc(security="BearerAuth")
    @api.expect(question_create_model)
    @api.response(201, "Вопрос создан", question_response_model)
    @api.response(400, "Нет текста")
    @api.response(403, "Только преподаватели")
    def post(self, group_id):
        user_id, role = _get_auth_info()
        if role != "teacher":
            api.abort(403, "Только преподаватели могут задавать вопросы")
        data = api.payload
        text = data.get("text", "").strip()
        if not text:
            api.abort(400, "Текст вопроса обязателен")
        question = create_question(text=text, teacher_id=user_id, group_id=group_id)
        return question.to_dict(include_teacher=True), 201

@api.route("/questions/<int:question_id>")
class Question(Resource):
    @api.doc(security="BearerAuth")
    @api.response(204, "Удалено")
    @api.response(403, "Только автор")
    @api.response(404, "Не найдено")
    def delete(self, question_id):
        user_id, role = _get_auth_info()
        if role not in ("teacher", "admin"):
            api.abort(403)
        success = delete_question(question_id, teacher_id=user_id)
        if not success:
            api.abort(404, "Вопрос не найден или вы не его автор")
        return "", 204

@api.route("/questions/<int:question_id>/answers")
class QuestionAnswers(Resource):
    @api.doc(security="BearerAuth")
    @api.expect(answer_create_model)
    @api.response(201, "Ответ добавлен", answer_response_model)
    @api.response(403, "Только студенты")
    def post(self, question_id):
        user_id, role = _get_auth_info()
        if role != "student":
            api.abort(403, "Только студенты могут отвечать")
        data = api.payload
        text = data.get("text", "").strip()
        if not text:
            api.abort(400, "Текст ответа обязателен")
        answer = create_answer(text=text, student_id=user_id, question_id=question_id)
        if not answer:
            api.abort(404, "Вопрос не найден")
        return answer.to_dict(), 201

    @api.doc(security="BearerAuth")
    @api.param("page", "Страница", _in="query")
    @api.param("limit", "Лимит", _in="query")
    @api.response(200, "OK", [answer_response_model])
    @api.response(403, "Только преподаватель/админ")
    def get(self, question_id):
        user_id, role = _get_auth_info()
        if role not in ("teacher", "admin"):
            api.abort(403, "Студенты не могут просматривать ответы")
        page = max(1, int(request.args.get("page", 1)))
        limit = min(100, max(1, int(request.args.get("limit", 20))))
        answers, total = get_answers_by_question(question_id, page=page, limit=limit)
        return [a.to_dict(include_student=True) for a in answers], 200