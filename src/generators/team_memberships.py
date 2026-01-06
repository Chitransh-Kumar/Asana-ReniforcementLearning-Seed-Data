import random
from datetime import datetime

from utils.dates import random_past_date

def generate_team_memberships(conn, users, teams):
    cursor = conn.cursor()

    # Fetch organization creation DATE
    cursor.execute("SELECT created_at FROM organizations")
    org_created_at = datetime.fromisoformat(cursor.fetchone()[0]).date()

    memberships = []
    seen = set()

    for user in users:
        user_id = user["user_id"]

        # Each user belongs to 1–3 teams
        num_teams = random.choices(
            [1, 2, 3],
            weights=[0.6, 0.3, 0.1]
        )[0]

        assigned_teams = random.sample(teams, min(num_teams, len(teams)))

        for team in assigned_teams:
            team_id = team["team_id"]

            key = (team_id, user_id)
            if key in seen:
                continue

            # Fetch team creation DATE
            cursor.execute(
                "SELECT created_at FROM teams WHERE team_id = ?",
                (team_id,)
            )
            team_created_at = datetime.fromisoformat(cursor.fetchone()[0]).date()

            joined_at = random_past_date(
                min_days_ago=365 * 2,
                max_days_ago=365 * 4
            )

            # Enforce temporal consistency
            earliest_allowed = max(org_created_at, team_created_at)
            if joined_at < earliest_allowed:
                joined_at = earliest_allowed

            cursor.execute(
                """
                INSERT INTO team_memberships (team_id, user_id, joined_at)
                VALUES (?, ?, ?)
                """,
                (team_id, user_id, joined_at.isoformat())
            )

            memberships.append({
                "team_id": team_id,
                "user_id": user_id
            })
            seen.add(key)

    conn.commit()
    return memberships
