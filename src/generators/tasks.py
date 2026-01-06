import random
from datetime import timedelta

from utils.uuid import generate_uuid
from utils.dates import random_past_datetime
from constants.task_templates import TASK_TITLES, COMPONENTS, TASK_DESCRIPTIONS
from constants.completion_rates import COMPLETION_RATES
from config.settings import (
    MIN_TASKS_PER_PROJECT,
    MAX_TASKS_PER_PROJECT,
    UNASSIGNED_TASK_PROBABILITY
)

def generate_tasks(conn, projects, sections, team_memberships):
    cursor = conn.cursor()
    tasks = []

    project_sections = {}
    for s in sections:
        project_sections.setdefault(s["project_id"], []).append(s["section_id"])

    # Pre-map users per team to ensure assignments stay within team boundaries
    team_users = {}
    for tm in team_memberships:
        team_users.setdefault(tm["team_id"], []).append(tm["user_id"])

    for project in projects:
        project_id = project["project_id"]
        project_type = project["project_type"]

        num_tasks = random.randint(
            MIN_TASKS_PER_PROJECT,
            MAX_TASKS_PER_PROJECT
        )

         # Completion likelihood varies by project type
        completion_min, completion_max = COMPLETION_RATES[project_type]
        completion_prob = random.uniform(completion_min, completion_max)

        for _ in range(num_tasks):
            task_id = generate_uuid()

            section_id = random.choice(project_sections[project_id])

            title_template = random.choice(TASK_TITLES[project_type])
            name = title_template.format(
                component=random.choice(COMPONENTS)
            )

            description = random.choice(TASK_DESCRIPTIONS)

            # Explicitly model unassigned backlog and triage work
            if random.random() < UNASSIGNED_TASK_PROBABILITY:
                assignee_id = None
            else:
                team_id = project["team_id"]
                assignee_id = random.choice(team_users.get(team_id, [None]))

            created_at = random_past_datetime(7, 180)
            completed = random.random() < completion_prob

            if random.random() < 0.1:
                due_date = None
            else:
                due_date = created_at + timedelta(
                    days=random.choice([3, 7, 14, 30, 60, 90])
                )

            completed_at = None
            if completed:
                completed_at = created_at + timedelta(
                    days=random.randint(1, 14)
                )

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
                    created_at.isoformat(),
                    completed_at.isoformat() if completed_at else None
                )
            )

            tasks.append({
                "task_id": task_id,
                "project_id": project_id
            })

    conn.commit()
    return tasks
