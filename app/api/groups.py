from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.group_service import create_group, get_all_groups
from app.services.auth_service import decode_jwt_token

api = Namespace("Groups", description="Управление учебными группами")

# Модель для документации и валидации
group_model = api.model("Group", {
    "name": fields.String(required=True, example="МАТ-303"),
    "faculty": fields.String(required=True, example="Математический факультет")
})

group_response_model = api.model("GroupResponse", {
    "id": fields.Integer(example=3),
    "name": fields.String(example="МАТ-303"),
    "faculty": fields.String(example="Математический факультет")
})

def _get_user_role_from_token() -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        api.abort(401, "Требуется аутентификация")
    token = auth_header.split(" ")[1]
    payload = decode_jwt_token(token)
    if not payload:
        api.abort(401, "Невалидный или просроченный токен")
    return payload["role"]

@api.route("/groups")
class Groups(Resource):
    @api.doc(security="BearerAuth")
    @api.param("page", "Номер страницы", _in="query", type="integer", default=1)
    @api.param("limit", "Количество на странице", _in="query", type="integer", default=20)
    @api.response(200, "Список групп", [group_response_model])
    @api.response(401, "Неавторизован")
    def get(self):
        page = max(1, int(request.args.get("page", 1)))
        limit = min(100, max(1, int(request.args.get("limit", 20))))
        groups, total = get_all_groups(page=page, limit=limit)
        return [g.to_dict() for g in groups], 200

    @api.doc(security="BearerAuth")
    @api.expect(group_model)
    @api.response(201, "Группа создана", group_response_model)
    @api.response(400, "Некорректные данные")
    @api.response(401, "Неавторизован")
    @api.response(403, "Только администраторы могут создавать группы")
    def post(self):
        role = _get_user_role_from_token()
        if role != "admin":
            api.abort(403, "Только администраторы могут создавать группы")

        data = api.payload
        name = data.get("name")
        faculty = data.get("faculty")

        if not name or not faculty:
            api.abort(400, "Поля 'name' и 'faculty' обязательны")

        group = create_group(name=name, faculty=faculty)
        return group.to_dict(), 201
    
    def get(self):
        _get_user_role_from_token()  

        page = max(1, int(request.args.get("page", 1)))
        limit = min(100, max(1, int(request.args.get("limit", 20))))
        groups, total = get_all_groups(page=page, limit=limit)
        return [g.to_dict() for g in groups], 200