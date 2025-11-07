from typing import List, Tuple
from app.models.reward import Reward

_rewards_db = {}
_next_reward_id = 1

def create_reward(name: str, description: str, cost: int, category: str = "other") -> Reward:
    global _next_reward_id
    if cost < 0:
        raise ValueError("cost must be non-negative")
    reward = Reward(_next_reward_id, name, description, cost, category)
    _rewards_db[reward.id] = reward
    _next_reward_id += 1
    return reward

def get_rewards(page: int = 1, limit: int = 20) -> Tuple[List[Reward], int]:
    rewards = list(_rewards_db.values())
    total = len(rewards)
    start = (page - 1) * limit
    end = start + limit
    return rewards[start:end], total