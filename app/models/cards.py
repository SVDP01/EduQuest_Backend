from dataclasses import dataclass

@dataclass
class Card:
    id: int
    front_text: str
    back_text: str
    subject: str
    topic: str

    def to_dict(self):
        return {
            "id": self.id,
            "front_text": self.front_text,
            "back_text": self.back_text,
            "subject": self.subject,
            "topic": self.topic
        }