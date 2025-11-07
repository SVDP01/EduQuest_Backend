from typing import List
from app.models.cards import Card

_cards_db = {}
_next_card_id = 1

def create_card(front_text: str, back_text: str, subject: str, topic: str) -> Card:
    global _next_card_id
    card = Card(_next_card_id, front_text, back_text, subject, topic)
    _cards_db[card.id] = card
    _next_card_id += 1
    return card

def get_cards(subject: str = None, topic: str = None) -> List[Card]:
    cards = list(_cards_db.values())
    if subject:
        cards = [c for c in cards if c.subject.lower() == subject.lower()]
    if topic:
        cards = [c for c in cards if c.topic.lower() == topic.lower()]
    return cards