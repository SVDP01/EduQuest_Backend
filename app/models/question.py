from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Question:
    id: int
    text: str
    teacher_id: int
    group_id: int
    created_at: datetime
    is_active: bool = True

    def to_dict(self, include_teacher: bool = False):
        res = {
            "id": self.id,
            "text": self.text,
            "group_id": self.group_id,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active
        }
        if include_teacher:
            res["teacher_id"] = self.teacher_id
        return res