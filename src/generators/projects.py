import random
from datetime import timedelta

from utils.uuid import generate_uuid
from utils.dates import random_past_datetime
from constants.project_types import PROJECT_TYPES
from constants.project_names import PROJECT_NAME_TEMPLATES
from config.settings import MIN_PROJECTS_PER_TEAM, MAX_PROJECTS_PER_TEAM

def generate_projects(conn, teams):
    cursor = conn.cursor()
    projects = []

    for team in teams:
        team_id = team["team_id"]

        # Each team owns multiple concurrent projects to reflect real Asana usage
        num_projects = random.randint(
            MIN_PROJECTS_PER_TEAM,
            MAX_PROJECTS_PER_TEAM
        )

        for _ in range(num_projects):
            project_id = generate_uuid()
            project_type = random.choice(PROJECT_TYPES)

            template = random.choice(PROJECT_NAME_TEMPLATES[project_type])
            name = template.format(
                q=random.randint(1, 4),
                w=random.randint(1, 12),
                year=2025,
                quarter=random.choice(["Q1", "Q2", "Q3", "Q4"]),
                product=random.choice(["Platform", "Integrations", "Automation"])
            )

            start_date = random_past_datetime(30, 365).date()

            # Only time-boxed initiatives receive explicit end dates
            if project_type in ["Sprint", "Marketing Campaign"]:
                duration_days = random.randint(14, 90)
                end_date = start_date + timedelta(days=duration_days)
            else:
                end_date = None

            created_at = start_date

            cursor.execute(
                """
                INSERT INTO projects
                (project_id, team_id, name, project_type, start_date, end_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    project_id,
                    team_id,
                    name,
                    project_type,
                    start_date.isoformat(),
                    end_date.isoformat() if end_date else None,
                    created_at.isoformat()
                )
            )

            projects.append({
                "project_id": project_id,
                "project_type": project_type,
                "team_id": team_id
            })

    conn.commit()
    return projects
