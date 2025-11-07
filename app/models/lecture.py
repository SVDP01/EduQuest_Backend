from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.models.group import Group
from app.models.user import User

@dataclass
class Lecture:
    id: int
    title: str
    description: str
    group: Group
    teacher: User
    scheduled_at: datetime
    duration_minutes: int = 90

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "group": self.group.to_dict(),
            "teacher": {
                "id": self.teacher.id,
                "first_name": self.teacher.first_name,
                "last_name": self.teacher.last_name,
                "role": self.teacher.role,
                # email и points не возвращаем для приватности (по аналогии с API)
            },
            "scheduled_at": self.scheduled_at.isoformat(),
            "duration_minutes": self.duration_minutes
        }