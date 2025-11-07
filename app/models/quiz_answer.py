from dataclasses import dataclass

@dataclass
class QuizAnswer:
    question_id: int
    selected_option_index: int

@dataclass
class QuizResult:
    total_points: int
    correct_answers: int
    total_questions: int
    earned_points: int