from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.reward_service import create_reward, get_rewards
from app.services.auth_service import decode_jwt_token

api = Namespace("Rewards", description="Награды и обмен баллов")

reward_model = api.model("Reward", {
    "name": fields.String(required=True, example="Футболка"),
    "description": fields.String(example="Хлопковая футболка с логотипом"),
    "cost": fields.Integer(required=True, min=0, example=100),
    "category": fields.String(default="merch", example="merch")
})

@api.route("/rewards")
class Rewards(Resource):
    @api.doc(security="BearerAuth")
    @api.param("page", "Страница", _in="query", type="integer", default=1)
    @api.param("limit", "Лимит", _in="query", type="integer", default=20)
    def get(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            api.abort(401)
        token = auth_header.split(" ")[1]
        payload = decode_jwt_token(token)
        if not payload:
            api.abort(401)

        page = max(1, int(request.args.get("page", 1)))
        limit = min(100, max(1, int(request.args.get("limit", 20))))
        rewards, total = get_rewards(page=page, limit=limit)
        return [r.to_dict() for r in rewards], 200

    @api.doc(security="BearerAuth")
    @api.expect(reward_model)
    def post(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            api.abort(401)
        token = auth_header.split(" ")[1]
        payload = decode_jwt_token(token)
        if not payload or payload["role"] != "admin":
            api.abort(403, "Только администраторы могут создавать награды")

        data = api.payload
        try:
            reward = create_reward(
                name=data["name"],
                description=data.get("description", ""),
                cost=data["cost"],
                category=data.get("category", "other")
            )
        except ValueError as e:
            api.abort(400, str(e))
        return reward.to_dict(), 201