import random
from datetime import datetime, timedelta

from utils.uuid import generate_uuid
from utils.dates import random_past_timestamp
from config.settings import SUBTASK_PROBABILITY, MAX_SUBTASKS_PER_TASK
from generators.task_content import generate_task_title


def generate_subtasks(conn, tasks):
    cursor = conn.cursor()
    subtasks = []

    now = datetime.now()

    for task in tasks:
        # Only a subset of tasks have subtasks
        if random.random() > SUBTASK_PROBABILITY:
            continue

        parent_task_id = task["task_id"]

        cursor.execute(
            """
            SELECT assignee_id, due_date, created_at, completed
            FROM tasks
            WHERE task_id = ?
            """,
            (parent_task_id,)
        )
        row = cursor.fetchone()
        if not row:
            continue

        parent_assignee_id, parent_due_date, parent_created_at, parent_completed = row
        parent_created_at = datetime.fromisoformat(parent_created_at)

        num_subtasks = random.randint(1, MAX_SUBTASKS_PER_TASK)

        for _ in range(num_subtasks):
            subtask_id = generate_uuid()

            # Name from scraped task titles
            name = generate_task_title()

            # Assignee: inherit from parent, 10% unassigned
            if random.random() < 0.9:
                assignee_id = parent_assignee_id
            else:
                assignee_id = None

            # Due date: must be <= parent task due date
            due_date = None
            if parent_due_date:
                if isinstance(parent_due_date, str):
                    parent_due_date = datetime.fromisoformat(parent_due_date).date()

                offset_days = random.randint(0, 5)
                due_date = parent_due_date - timedelta(days=offset_days)

            # Created_at: always after parent task created_at
            created_at = parent_created_at + timedelta(
                days=random.randint(0, 5),
                hours=random.randint(1, 8)
            )

            if created_at > now:
                created_at = now - timedelta(minutes=random.randint(1, 60))

            # Completion: correlated with parent but not guaranteed
            completed = parent_completed and random.random() < 0.85

            cursor.execute(
                """
                INSERT INTO subtasks
                (subtask_id, parent_task_id, name, assignee_id,
                 due_date, completed, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    subtask_id,
                    parent_task_id,
                    name,
                    assignee_id,
                    due_date.isoformat() if due_date else None,
                    completed,
                    created_at.isoformat(sep=" ")
                )
            )

            subtasks.append({
                "subtask_id": subtask_id,
                "parent_task_id": parent_task_id
            })

    conn.commit()
    return subtasks
