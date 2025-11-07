from flask_restx import Namespace, Resource
from flask import request
from app.services.lecture_service import get_lectures_for_user
from app.services.auth_service import decode_jwt_token, get_user_by_id

api = Namespace("Lectures", description="Лекции и расписание")

@api.route("/lectures")
class Lectures(Resource):
    @api.doc(security="BearerAuth")
    @api.response(200, "Список лекций")
    @api.response(401, "Требуется аутентификация")
    def get(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            api.abort(401, "Требуется аутентификация")
        token = auth_header.split(" ")[1]
        payload = decode_jwt_token(token)
        if not payload:
            api.abort(401, "Невалидный токен")

        user = get_user_by_id(payload["user_id"])
        if not user:
            api.abort(404, "Пользователь не найден")

        lectures = get_lectures_for_user(user)
        return [l.to_dict() for l in lectures], 200