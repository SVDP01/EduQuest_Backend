from typing import List
from datetime import datetime
from app.models.feedback import Feedback

# Заглушечная БД
_feedback_db: List[Feedback] = []
_next_feedback_id = 1

def create_feedback(rating: int, comment: str, lecture_id: int, student_id: int) -> Feedback:
    global _next_feedback_id
    if not (1 <= rating <= 5):
        raise ValueError("Rating must be between 1 and 5")
    feedback = Feedback(
        id=_next_feedback_id,
        rating=rating,
        comment=comment,
        lecture_id=lecture_id,
        student_id=student_id,
        created_at=datetime.utcnow()
    )
    _feedback_db.append(feedback)
    _next_feedback_id += 1
    return feedback

def get_feedback_by_lecture(lecture_id: int) -> List[Feedback]:
    return [f for f in _feedback_db if f.lecture_id == lecture_id]

def get_feedback_stats(lecture_id: int) -> dict:
    feedbacks = get_feedback_by_lecture(lecture_id)
    if not feedbacks:
        return {"count": 0, "avg_rating": 0.0}
    ratings = [f.rating for f in feedbacks]
    return {
        "count": len(feedbacks),
        "avg_rating": round(sum(ratings) / len(ratings), 2),
        "distribution": {i: ratings.count(i) for i in range(1, 6)}
    }