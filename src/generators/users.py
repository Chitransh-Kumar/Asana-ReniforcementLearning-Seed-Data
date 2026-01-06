import random

from utils.uuid import generate_uuid
from utils.dates import random_past_date
from constants.roles import USER_ROLES
from config.settings import MIN_USERS, MAX_USERS
from scrapers.names import generate_full_names  


def generate_users(conn, org_id, domain):
    cursor = conn.cursor()

    num_users = random.randint(MIN_USERS, MAX_USERS)

    # Generate full names once using web-scraped sources
    full_names = generate_full_names(num_users)

    email_counter = {}
    users = []

    roles, weights = zip(*USER_ROLES)

    for full_name in full_names:
        user_id = generate_uuid()

        first, last = full_name.split(" ", 1)

        base_email = f"{first.lower()}.{last.lower()}@{domain}"

        # Ensure email uniqueness
        if base_email not in email_counter:
            email_counter[base_email] = 1
            email = base_email
        else:
            email_counter[base_email] += 1
            email = f"{first.lower()}.{last.lower()}{email_counter[base_email]}@{domain}"

        role = random.choices(roles, weights=weights)[0]

        created_at = random_past_date(
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
