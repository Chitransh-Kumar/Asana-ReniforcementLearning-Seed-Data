import random
from datetime import timedelta, datetime

from utils.uuid import generate_uuid
from utils.dates import random_past_date, random_past_timestamp
from generators.project_names import generate_project_name
from constants.project_types import PROJECT_TYPES
from config.settings import MIN_PROJECTS_PER_TEAM, MAX_PROJECTS_PER_TEAM


def generate_projects(conn, teams):
    cursor = conn.cursor()
    projects = []

    for team in teams:
        team_id = team["team_id"]

        # Each team owns multiple projects
        num_projects = random.randint(
            MIN_PROJECTS_PER_TEAM,
            MAX_PROJECTS_PER_TEAM
        )

        for _ in range(num_projects):
            project_id = generate_uuid()

            # Controlled vocabulary
            project_type = random.choice(PROJECT_TYPES)

            # Name from cached Asana + SaaS scraped templates
            name = generate_project_name()

            # Start date: within last 6–12 months
            start_date = random_past_date(
                min_days_ago=180,
                max_days_ago=365
            )

            # End date only for time-boxed projects
            if project_type in ["Sprint", "Marketing Campaign"]:
                duration_days = random.randint(14, 90)
                end_date = start_date + timedelta(days=duration_days)
            else:
                end_date = None

            # Created at: timestamp, always <= start_date
            created_at = random_past_timestamp(
                min_days_ago=180,
                max_days_ago=365
            )

            if created_at.date() > start_date:
                created_at = created_at.replace(
                    year=start_date.year,
                    month=start_date.month,
                    day=start_date.day
                )

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
                    created_at.isoformat(sep=" ")
                )
            )

            projects.append({
                "project_id": project_id,
                "team_id": team_id,
                "project_type": project_type
            })

    conn.commit()
    return projects
