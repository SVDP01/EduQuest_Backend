from dataclasses import dataclass
from typing import Optional

@dataclass
class Group:
    id: int
    name: str
    faculty: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "faculty": self.faculty
        }