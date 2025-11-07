from dataclasses import dataclass

@dataclass
class Reward:
    id: int
    name: str
    description: str = ""
    cost: int = 0
    category: str = "other"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "cost": self.cost,
            "category": self.category
        }