import random
from utils.dates import random_past_datetime

def generate_team_memberships(conn, users, teams):
    cursor = conn.cursor()

    memberships = []
    seen = set()

    for user in users:
        user_id = user["user_id"]

        # Skewed distribution to model matrix orgs without over-assigning users
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
            
            # Join dates predate most project activity to reflect stable teams
            joined_at = random_past_datetime(
                min_days_ago=365 * 2,
                max_days_ago=365 * 4
            )

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
