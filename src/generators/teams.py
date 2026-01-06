import random
from datetime import datetime
from utils.uuid import generate_uuid
from utils.dates import random_past_date
from constants.roles import TEAM_FUNCTIONS
from constants.workflows import TEAM_NAME_TEMPLATES

def generate_teams(conn, org_id):
    cursor = conn.cursor()

    # Fetch organization creation DATE
    cursor.execute(
        "SELECT created_at FROM organizations WHERE org_id = ?",
        (org_id,)
    )
    org_created_at = datetime.fromisoformat(cursor.fetchone()[0]).date()

    num_teams = random.randint(20, 40)
    teams = []

    for _ in range(num_teams):
        team_id = generate_uuid()

        function = random.choices(
            TEAM_FUNCTIONS,
            weights=[0.45, 0.2, 0.2, 0.15]
        )[0]

        team_name = random.choice(TEAM_NAME_TEMPLATES[function])

        created_at = random_past_date(
            min_days_ago=365 * 3,
            max_days_ago=365 * 5
        )

        # Enforce team created after organization
        if created_at < org_created_at:
            created_at = org_created_at

        cursor.execute(
            """
            INSERT INTO teams (team_id, org_id, name, function, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (team_id, org_id, team_name, function, created_at.isoformat())
        )

        teams.append({
            "team_id": team_id,
            "function": function
        })

    conn.commit()
    return teams
