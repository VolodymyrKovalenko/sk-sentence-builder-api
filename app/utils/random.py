import random
from datetime import date


def get_daily_random_ids(ids: list[int], count: int = 10) -> list[int]:
    seed = date.today().isoformat()
    rng = random.Random(seed)

    return rng.sample(ids, count)