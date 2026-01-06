import random
from datetime import timedelta, datetime

from utils.uuid import generate_uuid
from utils.dates import random_past_date, random_past_timestamp
from generators.task_content import (
    generate_task_title,
    generate_task_description
)
from constants.completion_rates import COMPLETION_RATES
from config.settings import (
    MIN_TASKS_PER_PROJECT,
    MAX_TASKS_PER_PROJECT,
    UNASSIGNED_TASK_PROBABILITY
)


def generate_tasks(conn, projects, sections, team_memberships):
    cursor = conn.cursor()
    tasks = []

    # Map sections per project
    project_sections = {}
    for s in sections:
        project_sections.setdefault(s["project_id"], []).append(s["section_id"])

    # Map users per team
    team_users = {}
    for tm in team_memberships:
        team_users.setdefault(tm["team_id"], []).append(tm["user_id"])

    now = datetime.now()

    for project in projects:
        project_id = project["project_id"]
        project_type = project["project_type"]
        team_id = project["team_id"]

        num_tasks = random.randint(
            MIN_TASKS_PER_PROJECT,
            MAX_TASKS_PER_PROJECT
        )

        completion_min, completion_max = COMPLETION_RATES[project_type]
        completion_prob = random.uniform(completion_min, completion_max)

        for _ in range(num_tasks):
            task_id = generate_uuid()

            section_id = random.choice(project_sections[project_id])

            name = generate_task_title()
            description = generate_task_description()

            # Assignee (15% unassigned)
            if random.random() < UNASSIGNED_TASK_PROBABILITY:
                assignee_id = None
            else:
                assignee_id = random.choice(team_users.get(team_id, [None]))

            # Created at (timestamp)
            created_at = random_past_timestamp(
                min_days_ago=7,
                max_days_ago=180
            )

            # Due date (DATE, 10% missing)
            if random.random() < 0.10:
                due_date = None
            else:
                due_date = (
                    created_at.date() +
                    timedelta(days=random.choice([3, 7, 14, 30, 60, 90]))
                )

            completed = random.random() < completion_prob

            completed_at = None
            if completed:
                completed_at = created_at + timedelta(
                    days=random.randint(1, 14)
                )

                # Ensure completed_at is before "now"
                if completed_at > now:
                    completed_at = now - timedelta(minutes=random.randint(1, 120))

            cursor.execute(
                """
                INSERT INTO tasks
                (task_id, project_id, section_id, name, description,
                 assignee_id, due_date, completed, created_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task_id,
                    project_id,
                    section_id,
                    name,
                    description,
                    assignee_id,
                    due_date.isoformat() if due_date else None,
                    completed,
                    created_at.isoformat(sep=" "),
                    completed_at.isoformat(sep=" ") if completed_at else None
                )
            )

            tasks.append({
                "task_id": task_id,
                "project_id": project_id
            })

    conn.commit()
    return tasks
