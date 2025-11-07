from dataclasses import dataclass
from datetime import datetime

@dataclass
class Answer:
    id: int
    text: str
    student_id: int
    question_id: int
    created_at: datetime

    def to_dict(self, include_student: bool = False, anonymize: bool = False):
        res = {
            "id": self.id,
            "text": self.text,
            "question_id": self.question_id,
            "created_at": self.created_at.isoformat()
        }
        if include_student:
            res["student_id"] = self.student_id
        if anonymize:
            res.pop("student_id", None)
        return res