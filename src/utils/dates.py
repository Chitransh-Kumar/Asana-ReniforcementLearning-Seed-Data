import random
from datetime import datetime, timedelta, timezone

def random_past_date(min_days_ago: int, max_days_ago: int):
    days_ago = random.randint(min_days_ago, max_days_ago)
    seconds_offset = random.randint(0, 86400)

    dt = datetime.now(timezone.utc) - timedelta(
        days=days_ago,
        seconds=seconds_offset
    )

    return dt.date()

def random_past_timestamp(min_days_ago: int, max_days_ago: int):
    days_ago = random.randint(min_days_ago, max_days_ago)
    seconds_offset = random.randint(0, 86400)

    dt = datetime.now() - timedelta(
        days=days_ago,
        seconds=seconds_offset
    )

    return dt.replace(microsecond=0)
