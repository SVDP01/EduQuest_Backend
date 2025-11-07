from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.card_service import create_card, get_cards
from app.services.auth_service import decode_jwt_token

api = Namespace("Cards", description="Карточки для повторения")

# Модель для создания карточки
card_model = api.model("Card", {
    "front_text": fields.String(required=True, example="Определение предела"),
    "back_text": fields.String(required=True, example="Число A называется пределом..."),
    "subject": fields.String(default="", example="Математический анализ"),
    "topic": fields.String(default="", example="Пределы")
})

# Модель ответа
card_response_model = api.model("CardResponse", {
    "id": fields.Integer(example=1),
    "front_text": fields.String(example="Определение предела"),
    "back_text": fields.String(example="Число A называется пределом..."),
    "subject": fields.String(example="Математический анализ"),
    "topic": fields.String(example="Пределы")
})

@api.route("/cards")  # ← именно так!
class Cards(Resource):
    @api.doc(security="BearerAuth")
    @api.param("subject", "Фильтр по предмету", _in="query", type="string")
    @api.param("topic", "Фильтр по теме", _in="query", type="string")
    @api.param("page", "Номер страницы", _in="query", type="integer", default=1)
    @api.param("limit", "Лимит на странице", _in="query", type="integer", default=20)
    @api.response(200, "Список карточек", [card_response_model])
    @api.response(401, "Неавторизован")
    def get(self):
        # Проверка токена
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            api.abort(401, "Требуется аутентификация")
        token = auth_header.split(" ")[1]
        payload = decode_jwt_token(token)
        if not payload:
            api.abort(401, "Невалидный токен")

        # Получаем параметры фильтрации
        subject = request.args.get("subject")
        topic = request.args.get("topic")
        page = max(1, int(request.args.get("page", 1)))
        limit = min(100, max(1, int(request.args.get("limit", 20))))

        # Получаем карточки
        cards = get_cards(subject=subject, topic=topic)
        total = len(cards)

        # Пагинация
        start = (page - 1) * limit
        end = start + limit
        paginated_cards = cards[start:end]

        return [c.to_dict() for c in paginated_cards], 200

    @api.doc(security="BearerAuth")
    @api.expect(card_model)
    @api.response(201, "Карточка создана", card_response_model)
    @api.response(400, "Некорректные данные")
    @api.response(403, "Только преподаватели могут создавать карточки")
    @api.response(401, "Неавторизован")
    def post(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            api.abort(401, "Требуется аутентификация")
        token = auth_header.split(" ")[1]
        payload = decode_jwt_token(token)
        if not payload:
            api.abort(401, "Невалидный токен")
        if payload["role"] != "teacher":
            api.abort(403, "Только преподаватели могут создавать карточки")

        data = api.payload
        front_text = data.get("front_text", "").strip()
        back_text = data.get("back_text", "").strip()
        subject = data.get("subject", "").strip()
        topic = data.get("topic", "").strip()

        if not front_text or not back_text:
            api.abort(400, "Поля 'front_text' и 'back_text' обязательны")

        # Создаём карточку
        card = create_card(
            front_text=front_text,
            back_text=back_text,
            subject=subject,
            topic=topic
        )

        return card.to_dict(), 201