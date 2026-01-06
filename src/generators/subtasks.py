import random
from datetime import datetime

from utils.uuid import generate_uuid
from utils.dates import random_past_datetime
from config.settings import SUBTASK_PROBABILITY, MAX_SUBTASKS_PER_TASK
from constants.subtask_templates import SUBTASK_TEMPLATES

def generate_subtasks(conn, tasks):
    cursor = conn.cursor()
    subtasks = []

    for task in tasks:
        # Only a subset of tasks are decomposed into subtasks
        if random.random() > SUBTASK_PROBABILITY:
            continue

        task_id = task["task_id"]

        cursor.execute(
            """
            SELECT assignee_id, due_date, created_at, completed
            FROM tasks
            WHERE task_id = ?
            """,
            (task_id,)
        )
        parent = cursor.fetchone()

        if not parent:
            continue

        num_subtasks = random.randint(1, MAX_SUBTASKS_PER_TASK)

        for _ in range(num_subtasks):
            subtask_id = generate_uuid()
            name = random.choice(SUBTASK_TEMPLATES)

            # Subtasks usually inherit ownership from the parent task
            if random.random() < 0.8:
                assignee_id = parent["assignee_id"]
            else:
                assignee_id = None

            due_date = None

            if parent["due_date"]:
                parent_due_date = datetime.fromisoformat(parent["due_date"]).date()

                # Subtask due dates constrained to not exceed parent task deadline
                candidate_due_date = random_past_datetime(0, 7).date()
                if candidate_due_date > parent_due_date:
                    due_date = parent_due_date
                else:
                    due_date = candidate_due_date

            completed = parent["completed"] and random.random() < 0.9

            created_at = random_past_datetime(1, 60)

            cursor.execute(
                """
                INSERT INTO subtasks
                (subtask_id, parent_task_id, name, assignee_id,
                 due_date, completed, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    subtask_id,
                    task_id,
                    name,
                    assignee_id,
                    due_date.isoformat() if due_date else None,
                    completed,
                    created_at.isoformat()
                )
            )

            subtasks.append({
                "subtask_id": subtask_id,
                "parent_task_id": task_id
            })

    conn.commit()
    return subtasks
