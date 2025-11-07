from dataclasses import dataclass
from typing import List

@dataclass
class Problem:
    id: int
    text: str
    difficulty: str  # "easy", "medium", "hard"
    subject: str
    solution_steps: List[str]
    correct_answer: str

    def to_dict(self, include_solution: bool = False):
        res = {
            "id": self.id,
            "text": self.text,
            "difficulty": self.difficulty,
            "subject": self.subject
        }
        if include_solution:
            res["solution_steps"] = self.solution_steps
            res["correct_answer"] = self.correct_answer
        return res
    
