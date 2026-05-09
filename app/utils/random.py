import random
from datetime import date


def get_daily_random_ids(ids: list[int], count: int = 10) -> list[int]:
    seed = date.today().isoformat()
    rng = random.Random(seed)

    sample_count = min(count, len(ids))
    return rng.sample(ids, sample_count)
