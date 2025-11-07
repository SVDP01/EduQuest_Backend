from flask import Flask
from flask_restx import Api
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация REST API
    authorizations = {
        "BearerAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": 'JWT token: prepend "Bearer "'
        }
    }

    api = Api(
        app,
        version="1.0",
        title="EduQuest API",
        description="Backend for EduQuest — education gamification platform",
        doc="/swagger",  # Swagger UI
        authorizations=authorizations,
        security="BearerAuth"
    )

    # Register namespaces
    from app.api.auth import api as auth_ns
    from app.api.users import api as users_ns
    from app.api.groups import api as groups_ns
    from app.api.questions import api as questions_ns
    from app.api.feedback import api as feedback_ns
    from app.api.cards import api as cards_ns
    from app.api.quiz import api as quiz_ns
    from app.api.trainer import api as trainer_ns
    from app.api.rewards import api as rewards_ns
    from app.api.lectures import api as lectures_ns
    api.add_namespace(lectures_ns, path="/api")
    api.add_namespace(rewards_ns, path="/api")
    api.add_namespace(trainer_ns, path="/api")
    api.add_namespace(quiz_ns, path="/api")
    api.add_namespace(cards_ns, path="/api")
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(users_ns, path="/api")
    api.add_namespace(groups_ns, path="/api")
    api.add_namespace(questions_ns, path="/api")
    api.add_namespace(feedback_ns, path="/api")
    return app

