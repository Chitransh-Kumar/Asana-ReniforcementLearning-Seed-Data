import random

from utils.uuid import generate_uuid
from utils.dates import random_past_datetime
from constants.roles import USER_ROLES
from constants.names import FIRST_NAMES, LAST_NAMES
from config.settings import MIN_USERS, MAX_USERS

def generate_users(conn, org_id, domain):
    cursor = conn.cursor()

    num_users = random.randint(MIN_USERS, MAX_USERS)

    email_counter = {}
    users = []

    roles, weights = zip(*USER_ROLES)

    for _ in range(num_users):
        user_id = generate_uuid()

        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        full_name = f"{first} {last}"

        base_email = f"{first.lower()}.{last.lower()}@{domain}"

        # ensure uniqueness
        if base_email not in email_counter:
            email_counter[base_email] = 1
            email = base_email
        else:
            email_counter[base_email] += 1
            email = f"{first.lower()}.{last.lower()}{email_counter[base_email]}@{domain}"

        # Role assignment follows weighted org-wide distribution
        role = random.choices(roles, weights=weights)[0]

        created_at = random_past_datetime(
            min_days_ago=365 * 2,
            max_days_ago=365 * 4
        )

        cursor.execute(
            """
            INSERT INTO users (user_id, org_id, full_name, email, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, org_id, full_name, email, role, created_at.isoformat())
        )

        users.append({
            "user_id": user_id,
            "role": role
        })

    conn.commit()
    return users
