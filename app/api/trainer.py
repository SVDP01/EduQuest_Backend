from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.trainer_service import create_problem, get_problems, solve_problem
from app.services.auth_service import decode_jwt_token

api = Namespace("Trainer", description="Тренажёр решения задач")

# Модели
problem_model = api.model("Problem", {
    "text": fields.String(required=True),
    "difficulty": fields.String(enum=["easy", "medium", "hard"], default="medium"),
    "subject": fields.String(default=""),
    "solution_steps": fields.List(fields.String, required=True),
    "correct_answer": fields.String(required=True)
})

problem_response_model = api.model("ProblemResponse", {
    "id": fields.Integer(),
    "text": fields.String(),
    "difficulty": fields.String(),
    "subject": fields.String()
})

solution_model = api.model("Solution", {
    "answer": fields.String(required=True)
})

solution_result_model = api.model("SolutionResult", {
    "is_correct": fields.Boolean(),
    "explanation": fields.String(),
    "points_earned": fields.Integer()
})

@api.route("/trainer/problems")
class TrainerProblems(Resource):
    @api.doc(security="BearerAuth")
    @api.param("difficulty", "Сложность")
    @api.param("subject", "Предмет")
    def get(self):
        # ... (проверка токена)
        payload = _auth()
        difficulty = request.args.get("difficulty")
        subject = request.args.get("subject")
        problems = get_problems(difficulty, subject)
        return [p.to_dict() for p in problems], 200

    @api.doc(security="BearerAuth")
    @api.expect(problem_model)
    def post(self):
        payload = _auth()
        if payload["role"] != "teacher":
            api.abort(403)
        data = api.payload
        try:
            problem = create_problem(**{k: v for k, v in data.items() if k in [
                "text", "difficulty", "subject", "solution_steps", "correct_answer"
            ]})
        except ValueError as e:
            api.abort(400, str(e))
        return problem.to_dict(include_solution=True), 201

@api.route("/trainer/problems/<int:id>/solve")
class SolveProblem(Resource):
    @api.doc(security="BearerAuth")
    @api.expect(solution_model)
    @api.marshal_with(solution_result_model)
    def post(self, id):
        payload = _auth()
        if payload["role"] != "student":
            api.abort(403)
        answer = api.payload.get("answer", "").strip()
        try:
            result = solve_problem(id, answer, payload["user_id"])
        except ValueError as e:
            api.abort(404, str(e))
        return result

# Вспомогательная функция
def _auth():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        api.abort(401)
    token = auth_header.split(" ")[1]
    payload = decode_jwt_token(token)
    if not payload:
        api.abort(401)
    return payload


