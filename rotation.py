import random

def generate_rotation(bounty_data: dict, seed: int):
    random.seed(seed)
    result = {}

    for tier, stages in bounty_data.items():
        shuffled = stages.copy()
        random.shuffle(shuffled)
        result[tier] = shuffled[:3]

    return result