import random
from datetime import datetime, timedelta, timezone

def random_past_datetime(min_days_ago: int, max_days_ago: int):
    days_ago = random.randint(min_days_ago, max_days_ago)
    seconds_offset = random.randint(0, 86400)

    return datetime.now(timezone.utc) - timedelta(
        days=days_ago,
        seconds=seconds_offset
    )
