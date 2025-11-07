from dataclasses import dataclass
from datetime import datetime

@dataclass
class Feedback:
    id: int
    rating: int  # 1–5
    comment: str
    lecture_id: int
    created_at: datetime
    # ⚠️ student_id НЕ сохраняем в to_dict() для анонимности
    student_id: int  # ← только для внутренней логики (если понадобится)

    def to_dict(self, include_student: bool = False):
        res = {
            "id": self.id,
            "rating": self.rating,
            "comment": self.comment,
            "lecture_id": self.lecture_id,
            "created_at": self.created_at.isoformat()
        }
        if include_student:
            res["student_id"] = self.student_id
        return res