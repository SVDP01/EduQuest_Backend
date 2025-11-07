from flask_restx import Namespace, Resource
from flask import request
from app.services.auth_service import decode_jwt_token, get_user_by_id

api = Namespace("Users", description="Управление пользователями")

@api.route("/users/me")
class CurrentUser(Resource):
    @api.doc(security="BearerAuth")
    @api.response(200, "OK")
    @api.response(401, "Неавторизован")
    def get(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            api.abort(401, "Требуется авторизация")
        token = auth_header.split(" ")[1]
        payload = decode_jwt_token(token)
        if not payload:
            api.abort(401, "Невалидный или просроченный токен")
        user = get_user_by_id(payload["user_id"])
        if not user:
            api.abort(404, "Пользователь не найден")
        return user.to_dict(), 200