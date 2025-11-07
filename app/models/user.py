from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class Group:
    id: int
    name: str
    faculty: Optional[str] = None

@dataclass
class User:
    id: int
    first_name: str
    last_name: str
    email: str
    password_hash: str  # для заглушки 
    role: str  # 'student', 'teacher', 'admin'
    points: int = 0
    group: Optional[Group] = None
    department: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role,
            "points": self.points,
            "group": self.group.__dict__ if self.group else None,
            "department": self.department
        }