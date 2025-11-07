from dataclasses import dataclass
from typing import List

@dataclass
class QuizQuestion:
    id: int
    text: str
    options: List[str]
    correct_answer: int  # индекс правильного ответа (0-based)
    points: int = 10

    def to_dict(self, include_correct: bool = False):
        res = {
            "id": self.id,
            "text": self.text,
            "options": self.options,
            "points": self.points
        }
        if include_correct:
            res["correct_answer"] = self.correct_answer
        return res